from flask import json


def test_creating_movie(client):
    response = client.post('/movies', data=json.dumps({
        'title': 'Home Alone',
    }), content_type='application/json')
    assert response.status_code == 201

    response = client.get('/movies')
    assert response.status_code == 200

    movies = json.loads(response.data)['items']
    titles = [m['title'] for m in movies]

    assert 'Home Alone' in titles
