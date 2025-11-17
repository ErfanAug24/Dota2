import pytest
from app import create_app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.model_mixin import ModelMixin
from app.models import Base


@pytest.fixture(scope="function")
def app():
    app = create_app(app_config="config.TestingConfig")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def session(app):
    # Create engine
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    Base.metadata.create_all(engine)

    # Start a connection and a transaction
    connection = engine.connect()
    transaction = connection.begin()

    # Bind a session to this connection
    Session = sessionmaker(bind=connection)
    sess = Session()
    ModelMixin.set_session(sess)

    yield sess  # test runs here

    # Rollback everything after test
    sess.close()
    transaction.rollback()
    connection.close()