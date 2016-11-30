from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from uuid import uuid4

from horse import models
from .movies import get_movie_by_pk, jsonify_movie


users = []

users_bp = Blueprint('users_api', __name__)
users_api = Api(users_bp)


def get_user_by_pk(user_pk):
    return [u for u in users if u.pk == user_pk][0]


def jsonify_user(user):
    return {
        'pk': user.pk,
        'name': user.name,
    }


class User(Resource):
    def get(self, user_pk):
        user = get_user_by_pk(user_pk)
        return jsonify({
            'following': [
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
            'items': [jsonify_user(u) for u in users]
        })

    def post(self):
        data = request.get_json()
        user = models.User(
            pk=str(uuid4()),
            name=data['name'],
        )
        users.append(user)
        return jsonify_user(user), 201


users_api.add_resource(UserList, '/users')


class UserFollow(Resource):
    def post(self, user_pk):
        data = request.get_json()
        user = get_user_by_pk(user_pk)
        user_to_follow = get_user_by_pk(data['pk'])
        user.add_to_followed_users(user_to_follow)
        return {}


users_api.add_resource(UserFollow, '/users/<string:user_pk>/follow')


class UserLikesMovie(Resource):
    def post(self, user_pk):
        data = request.get_json()
        user = get_user_by_pk(user_pk)
        movie = get_movie_by_pk(data['pk'])

        user.add_to_liked_movies(movie)


users_api.add_resource(UserLikesMovie, '/users/<string:user_pk>/liked_movies')
