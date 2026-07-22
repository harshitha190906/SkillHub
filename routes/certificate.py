from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
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
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@certificate.route("/certificates")
def certificates():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = Certificate.get_certificates(mysql, session["user_id"])

    return render_template("certificates.html", certificates=data)


@certificate.route("/certificates/upload", methods=["GET", "POST"])
def upload_certificate():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        title = request.form["title"]
        file = request.files["certificate"]

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            unique_name = f"{uuid.uuid4()}_{filename}"

            file.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    unique_name
                )
            )

            Certificate.add_certificate(
                mysql,
                session["user_id"],
                title,
                unique_name
            )

            return redirect(url_for("certificate.certificates"))

    return render_template("upload_certificate.html")
@certificate.route("/certificates/delete/<int:id>")
def delete_certificate(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    Certificate.delete_certificate(mysql, id)

    return redirect(url_for("certificate.certificates"))