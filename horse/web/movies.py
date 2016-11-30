from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

from horse import models


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
        movie = models.Movie(title=data['title'])
        g.repos.movies.store(movie)
        return jsonify_movie(movie), 201

    def get(self):
        return jsonify({
            'items': [jsonify_movie(m) for m in g.repos.movies.all()],
        })

movies_api.add_resource(Movie, '/movies')
