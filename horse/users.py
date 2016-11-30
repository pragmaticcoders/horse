from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from uuid import uuid4


users = []

users_bp = Blueprint('users_api', __name__)
users_api = Api(users_bp)


class UserList(Resource):
    def get(self):
        return jsonify({
            'items': users,
        })


users_api.add_resource(UserList, '/users')


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        user = {
            'id': str(uuid4()),
            'name': data['name'],
        }

        users.append(user)
        return user, 201


users_api.add_resource(UserRegistration, '/users/register')
