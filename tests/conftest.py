import pytest

from horse import build_app


@pytest.fixture(scope='session')
def app():
    return build_app()


@pytest.fixture
def client(app):
    client = app.test_client()
    client.testing = True
    return client
