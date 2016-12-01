from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

from horse import models
from .schemas.movie import movie_schema, movies_schema

movies_bp = Blueprint('movies_api', __name__)
movies_api = Api(movies_bp)


class Movie(Resource):
    def post(self):
        data, errors = movie_schema.load(request.get_json())
        if errors:
            return {'errors': errors}, 400
        movie = models.Movie(title=data['title'])
        g.repos.movies.store(movie)
        result = movie_schema.dump(movie).data
        return result, 201

    def get(self):
        movies = g.repos.movies.all()
        result = movies_schema.dump(movies)
        return jsonify({
            'items': result.data,
        })

movies_api.add_resource(Movie, '/movies')
