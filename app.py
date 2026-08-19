import pymysql
pymysql.install_as_MySQLdb()

from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)
from flask_mysqldb import MySQL
import os
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename
# pyrefly: ignore [missing-import]
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from utils.db_adapter import SmartMySQL

from routes.auth import auth, init_mysql
from routes.skills import skills, init_mysql as init_skill_mysql
from routes.certificate import certificate, init_mysql as init_certificate_mysql

app = Flask(__name__)

# Load configurations from Config object
app.config.from_object(Config)
app.secret_key = app.config.get("SECRET_KEY", "default_secret_key")



# Initialize MySQL with smart fallback
mysql = SmartMySQL(app)

# Initialize Blueprints
init_mysql(mysql)
init_skill_mysql(mysql)
init_certificate_mysql(mysql)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(skills)
app.register_blueprint(certificate)


def init_tables():
    """Auto-create DB tables if they don't exist (runs on startup)."""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                bio TEXT,
                profile_image VARCHAR(255)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                skill_name VARCHAR(255) NOT NULL,
                skill_level VARCHAR(50) NOT NULL,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS certificates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        mysql.connection.commit()
        cursor.close()
        print("[SUCCESS] Database tables verified/created successfully.")
    except Exception as e:
        print(f"[WARNING] Table init warning: {e}")


with app.app_context():
    init_tables()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:
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
        cursor.execute("""
            SELECT skill_name
            FROM skills
            WHERE user_id=%s
            ORDER BY id DESC
            LIMIT 1
        """, (session["user_id"],))

        latest = cursor.fetchone()
        latest_skill = latest[0] if latest else "No Skills"

        # Chart Data
        cursor.execute("""
            SELECT skill_level, COUNT(*)
            FROM skills
            WHERE user_id=%s
            GROUP BY skill_level
        """, (session["user_id"],))

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

    except Exception as e:
        return f"""
        <h2>Dashboard Error</h2>
        <pre>{e}</pre>
        """

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT fullname, email, profile_image
        FROM users
        WHERE id=%s
    """, (session["user_id"],))

    user = cursor.fetchone()

    cursor.close()

    return render_template("profile.html", user=user)

@app.route("/upload_profile", methods=["POST"])
def upload_profile():

    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Check if a file was submitted
    if "profile" not in request.files:
        flash("No file selected.", "danger")
        return redirect(url_for("profile"))

    file = request.files["profile"]

    # Check if filename is empty
    if file.filename == "":
        flash("Please choose an image.", "warning")
        return redirect(url_for("profile"))

    # Allowed image types
    allowed_extensions = {"png", "jpg", "jpeg"}

    if "." not in file.filename:
        flash("File must have a valid image extension.", "danger")
        return redirect(url_for("profile"))

    extension = file.filename.rsplit(".", 1)[1].lower()

    if extension not in allowed_extensions:
        flash("Only PNG, JPG and JPEG files are allowed.", "danger")
        return redirect(url_for("profile"))

    # Secure filename
    filename = secure_filename(file.filename)

    # Upload folder
    upload_folder = os.path.join(
        app.root_path,
        "static",
        "uploads",
        "profiles"
    )

    # Create folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)

    # Save file
    filepath = os.path.join(upload_folder, filename)

    print("Upload Folder:", upload_folder)
    print("Folder Exists:", os.path.exists(upload_folder))
    print("Saving File To:", filepath)

    file.save(filepath)

    # Save relative path in database
    image_path = f"uploads/profiles/{filename}"

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET profile_image=%s
        WHERE id=%s
        """,
        (image_path, session["user_id"])
    )

    mysql.connection.commit()
    cursor.close()

    flash("Profile picture updated successfully!", "success")

    return redirect(url_for("profile"))

# Optional Edit Profile Page
@app.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        fullname = request.form["fullname"].strip()
        bio = request.form.get("bio", "").strip()

        file = request.files.get("profile")

        cursor = mysql.connection.cursor()

        if file and file.filename != "" and "." in file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(app.root_path, "static", "uploads", "profiles")
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            image_path = f"uploads/profiles/{filename}"

            cursor.execute("""
                UPDATE users
                SET fullname=%s, bio=%s, profile_image=%s
                WHERE id=%s
            """, (fullname, bio, image_path, session["user_id"]))
        else:
            cursor.execute("""
                UPDATE users
                SET fullname=%s, bio=%s
                WHERE id=%s
            """, (fullname, bio, session["user_id"]))

        mysql.connection.commit()
        cursor.close()

        session["fullname"] = fullname

        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, fullname, email, password, bio, profile_image
        FROM users
        WHERE id=%s
    """, (session["user_id"],))
    user = cursor.fetchone()
    cursor.close()

    return render_template("edit_profile.html", user=user)


@app.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("settings.html")


# Change Password
@app.route("/change_password", methods=["POST"])
def change_password():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    if new_password != confirm_password:
        flash("Passwords do not match!", "danger")
        return redirect(url_for("settings"))

    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE id=%s",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    if not user:
        flash("User not found.", "danger")
        cursor.close()
        return redirect(url_for("settings"))

    db_password = user["password"] if isinstance(user, dict) else user[0]

    if not check_password_hash(db_password, current_password):
        flash("Current password is incorrect.", "danger")
        cursor.close()
        return redirect(url_for("settings"))

    hashed_password = generate_password_hash(new_password)

    cursor.execute(
        "UPDATE users SET password=%s WHERE id=%s",
        (hashed_password, session["user_id"])
    )

    mysql.connection.commit()
    cursor.close()

    flash("Password updated successfully!", "success")

    return redirect(url_for("settings"))


# Delete Account
@app.route("/delete_account", methods=["POST"])
def delete_account():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM certificates WHERE user_id=%s",
        (session["user_id"],)
    )

    cursor.execute(
        "DELETE FROM skills WHERE user_id=%s",
        (session["user_id"],)
    )

    cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (session["user_id"],)
    )

    mysql.connection.commit()
    cursor.close()

    session.clear()

    flash("Account deleted successfully.", "success")

    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)