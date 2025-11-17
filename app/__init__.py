import os
import sys
from flask import Flask
from app.extensions import init_extensions


def create_app(
    test_config_mapping: dict = None, app_config: str = "config.DevelopmentConfig"
) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    append_instance_path(app)

    if test_config_mapping is None:
        app.config.from_object("app." + app_config)
        app.config.from_pyfile("config.py", silent=True)
        init_extensions(app)
    else:
        app.config.update(test_config_mapping)

    app.route("/")(lambda: "Hello, World! This is a Flask application.")
    return app


def append_instance_path(app):
    if not sys.path.__contains__(app.instance_path):
        sys.path.append(app.instance_path)