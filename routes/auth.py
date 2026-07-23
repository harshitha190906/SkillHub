from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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

        fullname = request.form["fullname"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("auth.register"))

        # Check if username already exists
        existing_user = User.get_user_by_fullname(mysql, fullname)

        if existing_user:
            flash("Username already exists!", "warning")
            return redirect(url_for("auth.register"))

        # Check if email already exists
        existing_email = User.get_user_by_email(mysql, email)

        if existing_email:
            flash("Email already exists!", "warning")
            return redirect(url_for("auth.register"))

        User.create_user(mysql, fullname, email, password)

        flash("Registration Successful. Please Login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        fullname = request.form["fullname"].strip()
        password = request.form["password"]

        user = User.get_user_by_fullname(mysql, fullname)

        if user:

            if check_password_hash(user[3], password):

                session["user_id"] = user[0]
                session["fullname"] = user[1]
                session["email"] = user[2]

                flash(f"Welcome {user[1]}!", "success")

                return redirect(url_for("dashboard"))

        flash("Invalid Username or Password!", "danger")

        return redirect(url_for("auth.login"))

    return render_template("login.html")


# ---------------- LOGOUT ---------------- #

@auth.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("auth.login"))