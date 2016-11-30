def test_adding_user_to_followed(user, followed_user):
    followed_users = user.get_followed_users()
    assert len(followed_users) == 0

    user.add_to_followed_users(followed_user)
    followed_users = user.get_followed_users()
    assert len(followed_users) == 1
    assert followed_user in followed_users


def test_adding_movie_to_liked(user, movie):
    liked_movies = user.get_liked_movies()
    assert len(liked_movies) == 0

    user.add_to_liked_movies(movie)
    liked_movies = user.get_liked_movies()
    assert len(liked_movies) == 1
    assert movie in liked_movies
