from horse.models import User, Movie

import pytest


@pytest.fixture
def service(app):
    return app.ctx.recommendations.smart


def assert_recommendations(result, expected):
    def readable(lst):
        return [(item.pk, item.title) for item in lst]

    assert readable(result) == readable(expected)


def test_liked_movie_is_not_included(service, movies_repo):
    user = User('root')
    other = User('other')

    movie_a = Movie('a')
    movie_b = Movie('b')

    movies_repo.store(movie_a)
    movies_repo.store(movie_b)

    user.add_to_liked_movies(movie_a)
    other.add_to_liked_movies(movie_b)

    result = service.recommend(user)

    assert_recommendations(result, [movie_b])


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


def test_nested_follows_are_more_influential(service, movies_repo):
    movie_a = Movie('a')
    movie_b = Movie('b')

    movies_repo.store(movie_b)
    movies_repo.store(movie_a)

    user = User('root')
    followed_user_1 = User('followed 1')
    followed_user_2 = User('followed 2')

    user.add_to_followed_users(followed_user_1)
    user.add_to_followed_users(followed_user_2)
    followed_user_2.add_to_followed_users(followed_user_1)

    followed_user_1.add_to_liked_movies(movie_a)
    followed_user_2.add_to_liked_movies(movie_b)

    result = service.recommend(user)

    assert_recommendations(result, [movie_a, movie_b])


def test_similar_users_are_more_influential(service, movies_repo):
    movie_a = Movie('a')
    movie_b = Movie('b')
    movie_c = Movie('c')

    movies_repo.store(movie_a)
    movies_repo.store(movie_b)
    movies_repo.store(movie_c)

    user = User('root')
    followed_user_1 = User('followed 1')
    followed_user_2 = User('followed 2')

    user.add_to_followed_users(followed_user_1)
    user.add_to_followed_users(followed_user_2)

    followed_user_1.add_to_liked_movies(movie_a)
    followed_user_2.add_to_liked_movies(movie_b)
    followed_user_2.add_to_liked_movies(movie_c)

    # User shares a common movie with followed_user_2
    user.add_to_liked_movies(movie_c)

    result = service.recommend(user)

    assert_recommendations(result, [movie_b, movie_a])


def test_globally_liked_movies_are_more_influential(service, movies_repo):
    user = User('root')

    movie_a = Movie('a')
    movie_b = Movie('b')
    movie_c = Movie('c')

    movies_repo.store(movie_a)
    movies_repo.store(movie_b)
    movies_repo.store(movie_c)

    user_a = User('a')
    user_b = User('b')

    user_a.add_to_liked_movies(movie_a)
    user_a.add_to_liked_movies(movie_b)
    user_b.add_to_liked_movies(movie_b)

    result = service.recommend(user)

    assert_recommendations(result, [movie_b, movie_a])


def test_movie_without_likes_is_not_recommended(service, movies_repo):
    user = User('root')
    movie_a = Movie('a')
    movie_b = Movie('b')

    movies_repo.store(movie_a)
    movies_repo.store(movie_b)

    user.add_to_liked_movies(movie_b)

    result = service.recommend(user)

    assert_recommendations(result, [])
