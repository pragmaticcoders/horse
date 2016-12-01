from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

from horse import models
from .schemas.user import user_schema, users_schema, user_action_schema

users_bp = Blueprint('users_api', __name__)
users_api = Api(users_bp)


class User(Resource):
    def get(self, user_pk):
        user = g.repos.users.get(user_pk)
        result = user_schema.dump(user)
        return jsonify(result.data)

users_api.add_resource(User, '/users/<string:user_pk>')


class UserList(Resource):
    def get(self):
        users = g.repos.users.all()
        result = users_schema.dump(users)
        return jsonify({
            'items': result.data
        })

    def post(self):
        data, errors = user_schema.load(request.get_json())
        if errors:
            return {'errors': errors}, 400
        user = models.User(name=data['name'])
        g.repos.users.store(user)
        result = user_schema.dump(user)
        return result.data, 201


users_api.add_resource(UserList, '/users')


class UserFollow(Resource):
    def post(self, user_pk):
        data, errors = user_action_schema.load(request.get_json())
        if errors:
            return {'errors': errors}, 400
        user = g.repos.users.get(user_pk)
        user_to_follow = g.repos.users.get(data['pk'])
        user.add_to_followed_users(user_to_follow)


users_api.add_resource(UserFollow, '/users/<string:user_pk>/follow')


class UserLikesMovie(Resource):
    def post(self, user_pk):
        data = request.get_json()
        user = g.repos.users.get(user_pk)
        movie = g.repos.movies.get(data['pk'])

        user.add_to_liked_movies(movie)


users_api.add_resource(UserLikesMovie, '/users/<string:user_pk>/liked_movies')


class UserUnlikesMovie(Resource):
    def delete(self, user_pk, movie_pk):
        user = g.repos.users.get(user_pk)
        movie = g.repos.movies.get(movie_pk)

        user.remove_from_liked_movies(movie)
        return None, 204


users_api.add_resource(
    UserUnlikesMovie, '/users/<string:user_pk>/liked_movies/<string:movie_pk>'
)


class UserUnfollow(Resource):
    def delete(self, user_pk, other_user_pk):
        user = g.repos.users.get(user_pk)
        other_user = g.repos.users.get(other_user_pk)

        user.remove_from_followed_users(other_user)
        return None, 204


users_api.add_resource(
    UserUnfollow, '/users/<string:user_pk>/follow/<string:other_user_pk>'
)
