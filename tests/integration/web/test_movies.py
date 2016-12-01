from flask import json


def test_creating_movie(client):
    response = client.post('/movies', data=json.dumps({
        'title': 'Home Alone',
    }), content_type='application/json')
    assert response.status_code == 201

    response = client.get('/movies')
    assert response.status_code == 200

    movies = json.loads(response.data)['items']
    movie = movies[0]

    assert movie['title'] == 'Home Alone'
    assert movie['likes'] == 0


def test_creating_movie_400_error(client):
    response = client.post('/movies', data=json.dumps({
        'wrong_field': 'Home Alone',
    }), content_type='application/json')
    assert response.status_code == 400
