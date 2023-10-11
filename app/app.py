import os
import hashlib
import stripe
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
from emails import (
    send_email,
    send_notification_upload_email,
    send_email_to_admin,
)  # noqa: E501

load_dotenv()

SERVER_NAME = os.getenv("SERVER_NAME")
UPLOAD_FOLDER = os.getenv("APP_UPLOAD_FOLDER")
UPLOAD_FOLDER_MOUNT_PATH = os.getenv("UPLOAD_FOLDER_MOUNT_PATH")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
ALLOWED_EXTENSIONS_TIFF = {".tiff", ".tif"}
ALLOWED_EXTENSIONS_ECW = {".ecw"}
SEND_EMAIL = os.getenv("SEND_EMAIL")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("DEBUG")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SERVER_NAME"] = SERVER_NAME


def allowed_ecw_file_extension(filename):
    split = os.path.splitext(filename)
    file_extension = split[1].lower()
    return file_extension in ALLOWED_EXTENSIONS_ECW


def allowed_tiff_file_extension(filename):
    split = os.path.splitext(filename)
    session["paid"] = True
    file_extension = split[1].lower()
    return file_extension in ALLOWED_EXTENSIONS_TIFF


@app.route("/", methods=["GET"])
def home():
    return render_template("homepage.html")


@app.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file selected")
        return redirect(url_for("home"))
    email = escape(request.form["email"])
    file = request.files["file"]
    if file.filename == "":
        flash("No file selected")
        return redirect(url_for("home"))
    if email == "":
        flash("Please use an email")
        return redirect(url_for("home"))

    # converting tiff to COG
    if (
        file
        and allowed_tiff_file_extension(file.filename)
        or allowed_ecw_file_extension(file.filename)
    ):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        filename_hash = hashlib.md5(filename.encode("utf-8")).hexdigest()
        session["file"] = {
            "filename_hash": filename_hash,
            "filename": filename,
        }  # noqa: E501
        # Store filename_hash -> filename in the current session
        send_notification_upload_email()
        return redirect(
            url_for(
                "upload_complete",
                filename=filename,
                email=email,
            )
        )

    else:
        flash("Only .tiff, .tif or .ecw allowed")
        return redirect(url_for("home"))


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
        return redirect(url_for("home"))


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    session["has_paid"] = True
    new_name = filename.rsplit(".", 1)
    filename = new_name[0] + "_converted.tiff"
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/cancel-confirm/<filename>", methods=["GET"])
def cancel_confirm(filename):
    return """
    <h1>Are you sure you want to cancel?</h1>
    Your .tiff file cannot be downloaded without payment.

    <a href="{}">Proceed to payment</a>.
    """.format(
        url_for("payment", filename=filename)
    )


@app.route("/payment-complete/<filename>", methods=["GET"])
def payment_complete(filename):
    return redirect(url_for("download_file", filename=filename))


@app.route("/payment/<filename>", methods=["GET"])
def payment(filename):
    stripe.api_key = STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "USD",
                    "product_data": {
                        "name": "Your tiff download is ready",  # noqa: E501
                        "description": f"{filename.replace('.ecw', '.tiff')}",
                    },
                    "unit_amount": 50,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=f"{url_for('download_file', filename=filename, _scheme='https', _external=True)}",  # noqa: E501
        cancel_url=url_for(
            "cancel_confirm",
            filename=filename,
            _scheme="https",
            _external=True,  # noqa: E501
        ),  # noqa: E501
    )
    return redirect(checkout_session.url, code=303)


@background_task
def convert_ecw_to_cog(app=None, filename=None, email=None):
    print(f"Running background ecw to cog on {filename}")
    with app.app_context():
        subprocess.run(
            f"./ecw-to-COG.sh {filename} '{UPLOAD_FOLDER_MOUNT_PATH}'",
            shell=True,
        )
    if SEND_EMAIL == "True":
        send_email(email, filename)
        send_email_to_admin(email, filename)


@background_task
def convert_tif_to_cog(app=None, filename=None, email=None):
    print(f"Running background tif to cog on {filename}")
    with app.app_context():
        subprocess.run(
            f"./tif-to-COG.sh {filename} '{UPLOAD_FOLDER_MOUNT_PATH}'",
            shell=True,
        )
    if SEND_EMAIL == "True":
        send_email(email, filename)
        send_email_to_admin(email, filename)
