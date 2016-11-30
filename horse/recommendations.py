from flask import Blueprint, jsonify
from flask_restful import Resource, Api

from horse.recommendation.dummy_service import DummyRecommendationService
from horse.users import get_user_by_pk


recommendations_bp = Blueprint('recommendations_api', __name__)
recommendations_api = Api(recommendations_bp)


class Recommendations(Resource):
    def get(self, user_pk):
        user = get_user_by_pk(user_pk)
        recommended_movies = DummyRecommendationService().recommend(user)
        return jsonify({
            'items': [movie.title for movie in recommended_movies],
        })


recommendations_api.add_resource(
    Recommendations, '/users/<string:user_pk>/recommendations'
)
