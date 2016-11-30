from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from uuid import uuid4


movies = []

movies_bp = Blueprint('movies_api', __name__)
movies_api = Api(movies_bp)


class Movie(Resource):
    def post(self):
        data = request.get_json()
        movie = {
            'id': str(uuid4()),
            'name': data['name'],
        }

        movies.append(movie)
        return movie, 201

    def get(self):
        return jsonify({
            'items': movies,
        })

movies_api.add_resource(Movie, '/movies')
