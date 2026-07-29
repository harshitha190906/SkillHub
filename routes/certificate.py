from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    current_app,
    flash
)
from werkzeug.utils import secure_filename
from models.certificate import Certificate
import os
import uuid

certificate = Blueprint("certificate", __name__)

mysql = None


def init_mysql(db):
    global mysql
    mysql = db


ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ===========================
# View Certificates
# ===========================

@certificate.route("/certificates")
def certificates():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = Certificate.get_certificates(
        mysql,
        session["user_id"]
    )

    return render_template(
        "certificates.html",
        certificates=data
    )


# ===========================
# Upload Certificate
# ===========================

@certificate.route("/certificates/upload", methods=["GET", "POST"])
def upload_certificate():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        title = request.form["title"].strip()
        file = request.files.get("certificate")

        if not file or file.filename == "":
            flash("Please select a file.", "danger")
            return redirect(url_for("certificate.upload_certificate"))

        if not allowed_file(file.filename):
            flash("Only PDF, PNG, JPG and JPEG files are allowed.", "danger")
            return redirect(url_for("certificate.upload_certificate"))

        filename = secure_filename(file.filename)

        unique_name = f"{uuid.uuid4()}_{filename}"

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        os.makedirs(upload_folder, exist_ok=True)

        upload_path = os.path.join(
            upload_folder,
            unique_name
        )

        file.save(upload_path)

        Certificate.add_certificate(
            mysql,
            session["user_id"],
            title,
            unique_name
        )

        flash("Certificate uploaded successfully!", "success")

        return redirect(
            url_for("certificate.certificates")
        )

    return render_template("upload_certificate.html")


# ===========================
# Delete Certificate
# ===========================

@certificate.route("/certificates/delete/<int:id>")
def delete_certificate(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    Certificate.delete_certificate(
        mysql,
        id,
        session["user_id"]
    )

    flash("Certificate deleted successfully!", "success")

    return redirect(
        url_for("certificate.certificates")
    )