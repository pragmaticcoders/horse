from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

from horse import models
from .movies import get_movie_by_pk, jsonify_movie


users_bp = Blueprint('users_api', __name__)
users_api = Api(users_bp)


def jsonify_user(user):
    return {
        'pk': user.pk,
        'name': user.name,
    }


class User(Resource):
    def get(self, user_pk):
        user = g.repos.users.get(user_pk)
        return jsonify({
            'followed_users': [
                jsonify_user(u) for u in user.get_followed_users()
            ],
            'liked_movies': [
                jsonify_movie(m) for m in user.get_liked_movies()
            ],
        })

users_api.add_resource(User, '/users/<string:user_pk>')


class UserList(Resource):
    def get(self):
        return jsonify({
            'items': [jsonify_user(u) for u in g.repos.users.all()]
        })

    def post(self):
        data = request.get_json()
        user = models.User(name=data['name'])
        g.repos.users.store(user)
        return jsonify_user(user), 201


users_api.add_resource(UserList, '/users')


class UserFollow(Resource):
    def post(self, user_pk):
        data = request.get_json()
        user = g.repos.users.get(user_pk)
        user_to_follow = g.repos.users.get(data['pk'])
        user.add_to_followed_users(user_to_follow)
        return {}


users_api.add_resource(UserFollow, '/users/<string:user_pk>/follow')


class UserLikesMovie(Resource):
    def post(self, user_pk):
        data = request.get_json()
        user = g.repos.users.get(user_pk)
        movie = get_movie_by_pk(data['pk'])

        user.add_to_liked_movies(movie)


users_api.add_resource(UserLikesMovie, '/users/<string:user_pk>/liked_movies')
