def test_adding_user_to_followed(user, followed_user):
    followed_users = user.get_followed_users()
    assert len(followed_users) == 0

    user.add_to_followed_users(followed_user)
    followed_users = user.get_followed_users()
    assert len(followed_users) == 1
    assert followed_user in followed_users


def test_removing_user_from_followed(user, followed_user):
    user.add_to_followed_users(followed_user)
    followed_users = user.get_followed_users()
    assert len(followed_users) == 1
    assert followed_user in followed_users

    user.remove_from_followed_users(followed_user)
    followed_users = user.get_followed_users()
    assert len(followed_users) == 0


def test_adding_movie_to_liked(user, movie):
    liked_movies = user.get_liked_movies()
    assert len(liked_movies) == 0

    user.add_to_liked_movies(movie)
    liked_movies = user.get_liked_movies()
    assert len(liked_movies) == 1
    assert movie in liked_movies


def test_removing_movie_from_liked(user, movie):
    user.add_to_liked_movies(movie)
    liked_movies = user.get_liked_movies()
    assert len(liked_movies) == 1
    assert movie in liked_movies

    user.remove_from_liked_movies(movie)
    liked_movies = user.get_liked_movies()
    assert len(liked_movies) == 0
