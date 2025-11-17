from celery import Celery
import importlib
import pkgutil


celery = Celery(__name__)


def init_celery(app):
    celery.conf.update(app.config)
    app.celery = celery

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            if app is None:
                raise RuntimeError("Flask app has not been provided to Celery")
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def auto_import_tasks():
    package = __name__
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        importlib.import_module(f"{package}.{module_name}")


# auto_import_tasks()
