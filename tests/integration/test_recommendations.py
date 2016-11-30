from flask import json


def test_get_recommendations(client, user, followed_user, movie, users_repo):
    followed_user.add_to_liked_movies(movie)
    user.add_to_followed_users(followed_user)

    users_repo.store(user)
    users_repo.store(followed_user)

    response = client.get('/users/{}/recommendations'.format(user.pk))
    assert response.status_code == 200

    recommended_movies = json.loads(response.data)['items']

    assert movie.title in recommended_movies
