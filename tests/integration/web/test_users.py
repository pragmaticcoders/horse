from flask import json

from horse.models import User


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


def test_user_registration_400_error(client):
    response = client.post('/users', data=json.dumps({
        'name2': 'Kevin',
    }), content_type='application/json')
    assert response.status_code == 400


def test_user_can_follow_another_user(client, users_repo):
    eve = User(name='Eve')
    adam = User(name='Adam')
    users_repo.store(eve)
    users_repo.store(adam)

    response = client.post('/users/{}/follow'.format(eve.pk), data=json.dumps({
        'pk': adam.pk
    }), content_type='application/json')
    assert response.status_code == 200

    response = client.get('/users/{}'.format(eve.pk))
    assert response.status_code == 200

    followed_users = json.loads(response.data)['followed_users']
    followed_users_names = [u['name'] for u in followed_users]

    assert 'Adam' in followed_users_names


def test_user_follow_another_user_400_error(client):
    response = client.post('/users/1/follow', data=json.dumps({
        'user_pk': '2',
    }), content_type='application/json')
    assert response.status_code == 400


def test_user_can_like_movie(client, movie, user, users_repo, movies_repo):
    url = '/users/{user_pk}/liked_movies'.format(
        user_pk=user.pk,
    )
    assert movie.likes == 0
    response = client.post(url, data=json.dumps({
        'pk': movie.pk,
    }), content_type='application/json')
    assert response.status_code == 200

    response = client.get('/users/{}'.format(user.pk))
    liked_movies = json.loads(response.data)['liked_movies']
    movie_titles = [m['title'] for m in liked_movies]

    assert movie.title in movie_titles
    assert movie.likes == 1


def test_user_can_unlike_movie(client, movie, user, users_repo, movies_repo):
    user.add_to_liked_movies(movie)

    assert movie in user.get_liked_movies()
    assert movie.likes == 1

    response = client.delete(
        '/users/{}/liked_movies/{}'.format(user.pk, movie.pk)
    )
    assert response.status_code == 204

    assert len(user.get_liked_movies()) == 0
    assert movie.likes == 0
