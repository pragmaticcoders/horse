from flask import Blueprint, jsonify, g
from flask_restful import Resource, Api

from horse.web.schemas.movie import MovieSchema

recommendations_bp = Blueprint('recommendations_api', __name__)
recommendations_api = Api(recommendations_bp)

movies_schema = MovieSchema(many=True)


class Recommendations(Resource):
    def get(self, user_pk):
        user = g.repos.users.get(user_pk)
        recommended_movies = g.recommendations.dummy.recommend(user)
        result = movies_schema.dump(recommended_movies)
        return jsonify({'items': result.data})


recommendations_api.add_resource(
    Recommendations, '/users/<string:user_pk>/recommendations'
)
