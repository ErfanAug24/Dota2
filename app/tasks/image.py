from PIL import Image
import os
from ..extensions import celery


@celery.task
def get_image_information(file_path: str) -> dict:
    with Image.open(file_path) as img:
        width, height = img.size
        mode = img.mode
        format = img.format
        bit_depth = len(mode) * 8 if mode else None
        file_size = os.path.getsize(file_path)
        
    return {
        "resolution": f"{width}x{height}",
        "width": width,
        "height": height,
        "bit_depth": bit_depth,
        "file_size_kb": round(file_size / 1024, 2),
        "format": format,
        "mode": mode,
    }
