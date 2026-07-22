import os
from werkzeug.utils import secure_filename

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

def allowed_file(filename):
    """
    Check whether the uploaded file has an allowed extension.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_uploaded_file(file, upload_folder):
    """
    Save an uploaded file securely and return its filename.
    """
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filename


def get_skill_badge(level):
    """
    Return the Bootstrap badge class based on skill level.
    """
    badges = {
        "Beginner": "success",
        "Intermediate": "warning",
        "Advanced": "danger"
    }
    return badges.get(level, "secondary")