import os
import uuid

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
ALLOWED_PDF_EXTENSIONS = {"pdf"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_PDF_EXTENSIONS

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def get_extension(filename):
    """Returns the lowercase file extension without the dot, or '' if none."""
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[1].lower()


def is_allowed_file(filename):
    """Checks whether the file extension is one we accept."""
    return get_extension(filename) in ALLOWED_EXTENSIONS


def get_file_type(filename):
    """Returns 'image' or 'pdf' based on extension. Caller must validate first."""
    ext = get_extension(filename)
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return "image"
    return "pdf"


def generate_safe_filename(original_filename):
    """
    Generates a random, collision-proof filename while preserving the
    original extension. We never trust or reuse the user-supplied
    filename directly on disk (prevents path traversal / overwrite attacks).
    """
    ext = get_extension(original_filename)
    return f"{uuid.uuid4().hex}.{ext}"