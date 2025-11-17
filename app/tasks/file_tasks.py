from ..extensions import celery


@celery.tasks
def save_file(file, full_path: str):
    file.save(full_path)
