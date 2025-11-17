from ..models.media import MediaModel
from flask import current_app
from werkzeug.utils import secure_filename
import os, uuid
from ..tasks.image import get_image_information
from ..tasks.file_tasks import save_file


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def check_upload_path_exists(path) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=False)


def save_avatar_file(file) -> MediaModel:
    if not allowed_file(file.filename):
        raise ValueError("Unsupported file type.")
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    check_upload_path_exists(upload_dir)
    relative_path = os.path.join(upload_dir, unique_name)
    save_file(file, relative_path)
    image_info = get_image_information(relative_path)
    avatar = MediaModel.create(
        file_path=relative_path,
        file_type=image_info["format"],
        resolution=image_info["resolution"],
        width=image_info["width"],
        height=image_info["height"],
        file_size_kb=image_info["file_size_kb"],
        mode=image_info["mode"],
    )
    return avatar


def delete_avatar_file(avatar_id: int):
    avatar = MediaModel.get(avatar_id)
    if not avatar:
        raise ValueError("Avatar not found.")
    os.remove(avatar.file_path)
    avatar.remove()
