from uuid import uuid4
import pytest

from horse import build_app
from horse.models import Movie
from horse.models import User


@pytest.fixture(scope='session')
def app():
    return build_app(debug=True)


@pytest.fixture(scope='session')
def web_app(app):
    return app.web_app


@pytest.fixture(scope='session')
def users_repo(app):
    return app.ctx.repos.users


@pytest.fixture
def client(web_app):
    client = web_app.test_client()
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
    return Movie(str(uuid4()), 'Home alone')
