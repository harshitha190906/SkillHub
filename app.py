from flask import Flask, render_template, session, redirect, url_for
from flask_mysqldb import MySQL
from config import Config

from routes.auth import auth, init_mysql
from routes.skills import skills, init_mysql as init_skill_mysql
from routes.certificate import certificate, init_mysql as init_certificate_mysql

app = Flask(__name__)

app.config.from_object(Config)
app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER
app.secret_key = Config.SECRET_KEY

# Initialize MySQL
mysql = MySQL(app)

# Initialize Blueprints
init_mysql(mysql)
init_skill_mysql(mysql)
init_certificate_mysql(mysql)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(skills)
app.register_blueprint(certificate)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cursor = mysql.connection.cursor()

    # Total Skills
    cursor.execute(
        "SELECT COUNT(*) FROM skills WHERE user_id=%s",
        (session["user_id"],)
    )
    skill_count = cursor.fetchone()[0]

    # Total Certificates
    cursor.execute(
        "SELECT COUNT(*) FROM certificates WHERE user_id=%s",
        (session["user_id"],)
    )
    certificate_count = cursor.fetchone()[0]

    # Latest Skill
    cursor.execute(
        """
        SELECT skill_name
        FROM skills
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
        """,
        (session["user_id"],)
    )

    latest = cursor.fetchone()
    latest_skill = latest[0] if latest else "No Skills"

    # Chart Data
    cursor.execute(
        """
        SELECT skill_level, COUNT(*)
        FROM skills
        WHERE user_id=%s
        GROUP BY skill_level
        """,
        (session["user_id"],)
    )

    chart = cursor.fetchall()

    labels = [row[0] for row in chart]
    values = [row[1] for row in chart]

    cursor.close()

    return render_template(
        "dashboard.html",
        skill_count=skill_count,
        certificate_count=certificate_count,
        latest_skill=latest_skill,
        labels=labels,
        values=values
    )


@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("profile.html")


@app.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("settings.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)