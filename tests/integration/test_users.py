from flask import json


def test_user_registration(client):
    response = client.post('/users/register', data=json.dumps({
        'name': 'Kevin',
    }), content_type='application/json')
    assert response.status_code == 201

    response = client.get('/users')
    assert response.status_code == 200

    movies = json.loads(response.data)['items']
    names = [m['name'] for m in movies]

    assert 'Kevin' in names
