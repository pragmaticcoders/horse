from flask import json

from horse.users import users


def test_get_recommendations(client, user, followed_user, movie):
    followed_user.add_to_liked_movies(movie)
    user.add_to_followed_users(followed_user)
    users.extend([user, followed_user])

    response = client.get('/users/{}/recommendations'.format(user.pk))
    assert response.status_code == 200

    recommended_movies = json.loads(response.data)['items']

    assert movie.title in recommended_movies
