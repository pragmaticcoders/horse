from flask import json

from horse.models import Movie, User
from horse.users import users


def test_get_recommendations(client):
    user = User('3', 'John')
    second_user = User('4', 'Andrew')
    movie = Movie('Home alone')
    second_user.add_to_liked_movies(movie)
    user.add_to_followed_users(second_user)
    users.extend([user, second_user])

    response = client.get('/users/3/recommendations')
    assert response.status_code == 200

    recommended_movies = json.loads(response.data)['items']

    assert movie.title in recommended_movies
