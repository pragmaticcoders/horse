from flask import Blueprint, g, request
from flask_restful import Resource, Api

from horse import models

populate_bp = Blueprint('populate_api', __name__)
populate_api = Api(populate_bp)


class Populate(Resource):
    def post(self):
        self._clear_repositories()
        data = request.get_json()
        users_data = data['users']
        movies_data = data['movies']
        self._populate_users(users_data)
        self._populate_movies(movies_data)
        self._populate_relationships(users_data)
        return {}, 201

    def _clear_repositories(self):
        g.repos.users.clear()
        g.repos.movies.clear()

    def _populate_users(self, users_data):
        for user_data in users_data:
            user = models.User(name=user_data['name'])
            g.repos.users.store(user)

    def _populate_movies(self, movies_data):
        for movie_data in movies_data:
            movie = models.Movie(title=movie_data['title'])
            g.repos.movies.store(movie)

    def _populate_relationships(self, users_data):
        for user_data in users_data:
            user = g.repos.users.get_by_name(user_data['name'])
            self._populate_followed_users(user, user_data['followed_users'])
            self._populate_liked_movies(user, user_data['liked_movies'])

    def _populate_followed_users(self, user, followed_users_data):
        for followed_name in followed_users_data:
            followed_user = g.repos.users.get_by_name(followed_name)
            user.add_to_followed_users(followed_user)

    def _populate_liked_movies(self, user, liked_movies_data):
        for title in liked_movies_data:
            liked_movie = g.repos.movies.get_by_title(title)
            user.add_to_liked_movies(liked_movie)


populate_api.add_resource(
    Populate, '/populate'
)
