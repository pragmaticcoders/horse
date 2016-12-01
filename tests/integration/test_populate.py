import pytest
from flask import json


@pytest.fixture
def populate_feed():
    return {
        "users": [
            {
                "name": "John",
                "followed_users": ["Andrew"],
                "liked_movies": ["Shining", "Home alone"]
            },
            {
                "name": "Andrew",
                "followed_users": [],
                "liked_movies": []
            }
        ],
        "movies": [
            {"title": "Home alone"},
            {"title": "Shining"}
        ]
    }


def test_populate(client, populate_feed, users_repo, movies_repo):
    response = client.post(
        '/populate', data=json.dumps(populate_feed),
        content_type='application/json'
    )
    assert response.status_code == 201

    movies = movies_repo.all()
    titles = [m.title for m in movies]

    assert 'Home alone' in titles
    assert 'Shining' in titles

    users = users_repo.all()
    user_names = [u.name for u in users]

    assert 'Andrew' in user_names
    assert 'John' in user_names

    user = users_repo.get_by_name('John')
    followed_names = [followed.name for followed in user.get_followed_users()]
    assert 'Andrew' in followed_names

    liked_titles = [liked.title for liked in user.get_liked_movies()]
    assert 'Home alone' in liked_titles
    assert 'Shining' in liked_titles


def test_populate_400(client):
    response = client.post(
        '/populate', data=json.dumps({}), content_type='application/json'
    )
    assert response.status_code == 400
