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
    escape,
)
from werkzeug.utils import secure_filename
import subprocess
from dotenv import load_dotenv
from tasks import background_task
from emails import send_email

load_dotenv()

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS_TIFF = {".tiff", ".tif"}
ALLOWED_EXTENSIONS_ECW = {".ecw"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("DEBUG")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_ecw_file_extension(filename):
    split = os.path.splitext(filename)
    file_extension = split[1].lower()
    return file_extension in ALLOWED_EXTENSIONS_ECW


def allowed_tiff_file_extension(filename):
    split = os.path.splitext(filename)
    file_extension = split[1].lower()
    return file_extension in ALLOWED_EXTENSIONS_TIFF


@app.route("/", methods=["GET"])
def home():
    return render_template("homepage.html")


@app.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file selected")
        return redirect(request.url)
    email = escape(request.form["email"])
    file = request.files["file"]
    if file.filename == "":
        flash("No file selected")
        return redirect(request.url)
    if email == "":
        flash("Please use an email")
        return redirect(request.url)

    # converting tiff to COG
    if (
        file
        and allowed_tiff_file_extension(file.filename)
        or allowed_ecw_file_extension(file.filename)
    ):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        filename_hash = hashlib.md5(filename.encode("utf-8")).hexdigest()
        session["file"] = {"filename_hash": filename_hash, "filename": filename}
        # Store filename_hash -> filename in the current session
        return redirect(
            url_for(
                "upload_complete",
                filename=filename,
                email=email,
            )
        )

    else:
        flash("Only .tiff, .tif or .ecw allowed")
        return redirect(request.url)


@app.route("/upload-complete/<email>/<filename>", methods=["GET", "POST"])
def upload_complete(filename, email):
    flash("Map file converted!")
    if allowed_tiff_file_extension(filename):
        filename = secure_filename(filename)
        convert_tif_to_cog(filename=filename, email=email)
        return render_template("upload_complete.html")

    if allowed_ecw_file_extension(filename):
        filename = secure_filename(filename)
        convert_ecw_to_cog(filename=filename, email=email)

        return render_template("upload_complete.html")
    else:
        flash("Only .tiff, .tif or .ecw allowed")
        return render_template("homepage.html")


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    new_name = filename.rsplit(".", 1)
    filename = new_name[0] + "_converted.tiff"
    return send_from_directory(UPLOAD_FOLDER, filename)


@background_task
def convert_ecw_to_cog(app=None, filename=None, email=None):
    print(f"Running background ecw to cog on {filename}")
    with app.app_context():
        subprocess.run(
            f"./ecw-to-COG.sh {filename} {UPLOAD_FOLDER}",
            shell=True,
        )
    send_email(email, filename)
    # TODO: a function to send an email after this process is finished


@background_task
def convert_tif_to_cog(app=None, filename=None, email=None):
    print(f"Running background tif to cog on {filename}")
    with app.app_context():
        subprocess.run(
            f"./tif-to-COG.sh {filename} {UPLOAD_FOLDER}",
            shell=True,
        )
    send_email(email, filename)
    # TODO: a function to send an email after this process is finished
