import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # Flask Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    # MySQL Configuration
    MYSQL_HOST = os.getenv("DB_HOST", "localhost")
    MYSQL_USER = os.getenv("DB_USER", "root")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "")
    MYSQL_DB = os.getenv("DB_NAME", "skillhub")

    # File Upload Settings
    UPLOAD_FOLDER = os.path.join("static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # Allowed Upload Extensions
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

    # Flask-MySQLdb Options
    MYSQL_CURSORCLASS = "DictCursor"