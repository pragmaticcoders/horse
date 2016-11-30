from flask import json

from horse.users import users
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


def test_user_can_follow_another_user(client):
    users.extend([
        User(id='1', name='Eve'),
        User(id='2', name='Adam'),
    ])

    response = client.post('/users/1/follow', data=json.dumps({
        'id': '2',
    }), content_type='application/json')
    assert response.status_code == 200

    response = client.get('/users/1')
    assert response.status_code == 200

    following = json.loads(response.data)['following']
    following_names = [u['name'] for u in following]

    assert 'Adam' in following_names
