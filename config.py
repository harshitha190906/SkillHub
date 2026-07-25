import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Project root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)
print("===================================")
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_NAME:", os.getenv("DB_NAME"))
print("===================================")

class Config:
    # ==========================
    # Flask Configuration
    # ==========================
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    # ==========================
    # MySQL Configuration
    # ==========================
    MYSQL_HOST = os.getenv("DB_HOST")
    MYSQL_PORT = int(os.getenv("DB_PORT", 3306))
    MYSQL_USER = os.getenv("DB_USER")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
    MYSQL_DB = os.getenv("DB_NAME")

    # ==========================
    # Upload Configuration
    # ==========================
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    DEFAULT_PROFILE_IMAGE = "images/avatar.png"

    # ==========================
    # Flask Settings
    # ==========================
    SESSION_PERMANENT = False
    TEMPLATES_AUTO_RELOAD = True