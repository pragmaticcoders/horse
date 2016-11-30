from flask import json

from horse.models import User
from horse.web.movies import movies


def test_user_registration(client):
    response = client.post('/users', data=json.dumps({
        'name': 'Kevin',
    }), content_type='application/json')
    assert response.status_code == 201

    response = client.get('/users')
    assert response.status_code == 200

    movies = json.loads(response.data)['items']
    names = [m['name'] for m in movies]

    assert 'Kevin' in names


def test_user_can_follow_another_user(client, users_repo):
    users_repo.store(User(pk='1', name='Eve'))
    users_repo.store(User(pk='2', name='Adam'))

    response = client.post('/users/1/follow', data=json.dumps({
        'pk': '2',
    }), content_type='application/json')
    assert response.status_code == 200

    response = client.get('/users/1')
    assert response.status_code == 200

    followed_users = json.loads(response.data)['followed_users']
    followed_users_names = [u['name'] for u in followed_users]

    assert 'Adam' in followed_users_names


def test_user_can_like_movie(client, movie, user, users_repo):
    movies.append(movie)
    users_repo.store(user)

    url = '/users/{user_pk}/liked_movies'.format(
        user_pk=user.pk,
    )
    response = client.post(url, data=json.dumps({
        'pk': movie.pk,
    }), content_type='application/json')
    assert response.status_code == 200

    response = client.get('/users/{}'.format(user.pk))
    liked_movies = json.loads(response.data)['liked_movies']
    movie_titles = [m['title'] for m in liked_movies]

    assert movie.title in movie_titles
