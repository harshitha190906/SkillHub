from flask import Flask, render_template, session, redirect, url_for
from flask_mysqldb import MySQL
from config import Config
from routes.auth import auth, init_mysql
from routes.skills import skills
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

mysql = MySQL(app)

# Initialize MySQL in auth.py
init_mysql(mysql)
app.register_blueprint(auth)
app.register_blueprint(skills)
# Register Blueprint
app.register_blueprint(auth)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)