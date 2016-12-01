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


@pytest.fixture(scope='session')
def movies_repo(app):
    return app.ctx.repos.movies


@pytest.fixture(autouse=True)
def cleanup_data(users_repo, movies_repo):
    users_repo.clear()
    movies_repo.clear()


@pytest.fixture
def client(web_app):
    client = web_app.test_client()
    client.testing = True
    return client


@pytest.fixture
def user(users_repo):
    user = User('John')
    users_repo.store(user)
    return user


@pytest.fixture
def followed_user(users_repo):
    user = User('Andrew')
    users_repo.store(user)
    return user


@pytest.fixture
def movie(movies_repo):
    movie = Movie('Home alone')
    movies_repo.store(movie)
    return movie
