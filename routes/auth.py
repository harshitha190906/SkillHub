from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from models.user import User

auth = Blueprint("auth", __name__)

mysql = None

def init_mysql(db):
    global mysql
    mysql = db


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            return "Passwords do not match"

        existing = User.get_user_by_email(mysql, email)

        if existing:
            return "Email already exists"

        User.create_user(mysql, fullname, email, password)

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.get_user_by_email(mysql, email)

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["fullname"] = user[1]

            return redirect(url_for("dashboard"))

        return "Invalid Email or Password"

    return render_template("login.html")


@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))