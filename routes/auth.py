from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from models.user import User

auth = Blueprint("auth", __name__)

mysql = None


def init_mysql(db):
    global mysql
    mysql = db


# ---------------- REGISTER ---------------- #

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            return "Passwords do not match"

        # Check whether username already exists
        existing = User.get_user_by_fullname(mysql, fullname)

        if existing:
            return "Username already exists"

        User.create_user(mysql, fullname, email, password)

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        fullname = request.form["fullname"]
        password = request.form["password"]

        user = User.get_user_by_fullname(mysql, fullname)

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["fullname"] = user[1]
            session["email"] = user[2]

            return redirect(url_for("dashboard"))

        return "Invalid Username or Password"

    return render_template("login.html")


# ---------------- LOGOUT ---------------- #

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))