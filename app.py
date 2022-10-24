import os
import hashlib
from flask import (
    render_template,
    Flask,
    flash,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import subprocess
from dotenv import load_dotenv
from tasks import background_task

load_dotenv()

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS_TIFF = {"tiff", "tif"}
ALLOWED_EXTENSIONS_ECW = {"ecw"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("DEBUG")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_tiff_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS_TIFF
    )


def allowed_ecw_file(filename):
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS_ECW
    )


@app.route("/", methods=["GET"])
def home():
    return render_template("homepage.html")


@app.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file selected")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No file selected")
        return redirect(request.url)

    # converting tiff to COG
    if file and allowed_tiff_file(file.filename) or allowed_ecw_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        filename_hash = hashlib.md5(filename.encode("utf-8")).hexdigest()
        session["file"] = {"filename_hash": filename_hash, "filename": filename}
        # Store filename_hash -> filename in the current session
        return redirect(url_for("upload_complete", filename=filename))

    else:
        flash("Only .tiff, .tif or .ecw allowed")
        return redirect(request.url)


@app.route("/upload-complete/<filename>", methods=["GET", "POST"])
def upload_complete(filename):
    flash("Map file converted!")
    if allowed_tiff_file(filename):
        filename = secure_filename(filename)
        convert_tif_to_cog(filename=filename)

    if allowed_ecw_file(filename):
        filename = secure_filename(filename)
        convert_ecw_to_cog(filename=filename)

    return render_template("upload_complete.html", filename=filename)


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    new_name = filename.rsplit(".", 1)
    filename = new_name[0] + "_converted.tiff"
    return send_from_directory(UPLOAD_FOLDER, filename)


@background_task
def convert_ecw_to_cog(app=None, filename=None):
    print(f"Running background ecw to cog on {filename}")
    with app.app_context():
        subprocess.run(
            f"./ecw-to-COG.sh {filename} {UPLOAD_FOLDER}",
            shell=True,
        )
    # TODO: a function to send an email after this process is finished


@background_task
def convert_tif_to_cog(app=None, filename=None):
    print(f"Running background tif to cog on {filename}")
    with app.app_context():
        subprocess.run(
            f"./tif-to-COG.sh {filename} {UPLOAD_FOLDER}",
            shell=True,
        )
    # TODO: a function to send an email after this process is finished
