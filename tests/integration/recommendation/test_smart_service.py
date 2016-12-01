from horse.models import User, Movie

import pytest


@pytest.fixture
def service(app):
    return app.ctx.recommendations.smart


def assert_recommendations(result, expected):
    def readable(lst):
        return [(item.pk, item.title) for item in lst]

    assert readable(result) == readable(expected)


def test_followed_users_movie_is_more_influential(service, movies_repo):
    user = User('root')
    other_user = User('other')
    followed_user = User('followed')

    movie_a = Movie('a')
    movie_b = Movie('b')

    movies_repo.store(movie_a)
    movies_repo.store(movie_b)

    user.add_to_followed_users(followed_user)

    followed_user.add_to_liked_movies(movie_a)
    other_user.add_to_liked_movies(movie_b)

    result = service.recommend(user)

    assert_recommendations(result, [movie_a, movie_b])
