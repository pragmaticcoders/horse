import pytest

from horse import build_app
from horse.models import Movie
from horse.models import User


@pytest.fixture(scope='session')
def app():
    return build_app(debug=True)


@pytest.fixture
def client(app):
    client = app.test_client()
    client.testing = True
    return client


@pytest.fixture
def user():
    return User('John')


@pytest.fixture
def followed_user():
    return User('Andrew')


@pytest.fixture
def movie():
    return Movie('Home alone')
