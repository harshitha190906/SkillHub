import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    # Flask Secret Key
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    # ==========================
    # MySQL Configuration
    # ==========================
    MYSQL_HOST = os.getenv("DB_HOST", "localhost")
    MYSQL_USER = os.getenv("DB_USER", "root")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "")
    MYSQL_DB = os.getenv("DB_NAME", "skillhub")

    # ==========================
    # Upload Configuration
    # ==========================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Profile pictures will be stored here:
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads",
        "profiles"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # Allowed image extensions
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    # Default profile image
    DEFAULT_PROFILE_IMAGE = "images/avatar.png"