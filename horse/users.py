from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from uuid import uuid4


users = []

users_bp = Blueprint('users_api', __name__)
users_api = Api(users_bp)


def get_user_by_id(user_id):
    return [u for u in users if u['id'] == user_id][0]


class User(Resource):
    def get(self, user_id):
        user = get_user_by_id(user_id)
        return jsonify({
            'following': user['following'],
        })

users_api.add_resource(User, '/users/<string:user_id>')


class UserList(Resource):
    def get(self):
        return jsonify({
            'items': users,
        })

    def post(self):
        data = request.get_json()
        user = {
            'id': str(uuid4()),
            'name': data['name'],
        }

        users.append(user)
        return user, 201


users_api.add_resource(UserList, '/users')


class UserFollow(Resource):
    def post(self, user_id):
        data = request.get_json()
        user = get_user_by_id(user_id)
        user_to_follow = get_user_by_id(data['id'])

        user['following'].append(user_to_follow)

        return {}


users_api.add_resource(UserFollow, '/users/<string:user_id>/follow')
