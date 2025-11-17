import pytest
from app import create_app

def test_app_conf(app):

    assert app.config["TESTING"] is True

def test_app_route(client):
    response = client.get("/")
    print(response.data)
    assert response.data == b"Hello, World! This is a Flask application."

