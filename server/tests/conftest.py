import pytest

from efimera import create_app
from efimera.extensions import db

@pytest.fixture()
def app():
    app = create_app(config_class='config.TestConfig')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
