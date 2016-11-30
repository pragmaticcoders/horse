from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from uuid import uuid4

from horse import models


movies = []

movies_bp = Blueprint('movies_api', __name__)
movies_api = Api(movies_bp)


def jsonify_movie(movie):
    return {
        'pk': movie.pk,
        'title': movie.title,
    }


class Movie(Resource):
    def post(self):
        data = request.get_json()
        movie = models.Movie(
            pk=str(uuid4()),
            title=data['title'],
        )
        movies.append(movie)
        return jsonify_movie(movie), 201

    def get(self):
        return jsonify({
            'items': [jsonify_movie(m) for m in movies],
        })

movies_api.add_resource(Movie, '/movies')
