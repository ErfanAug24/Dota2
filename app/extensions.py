from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from app.utils.model_mixin import ModelMixin
from app.models.base import Base
from .tasks import init_celery
import redis


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def init_extensions(app):
    init_celery(app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    ModelMixin.set_session(db.session)
    redis_client.ping()
    app.extensions["redis"] = redis_client
