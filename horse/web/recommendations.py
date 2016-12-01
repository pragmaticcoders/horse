from flask import Blueprint, jsonify, g
from flask_restful import Resource, Api

from .schemas.recommendation import recommendations_schema

recommendations_bp = Blueprint('recommendations_api', __name__)
recommendations_api = Api(recommendations_bp)


class Recommendations(Resource):
    def get(self, user_pk):
        user = g.repos.users.get(user_pk)
        recommendations = g.recommendations.smart.recommend(user)
        result = recommendations_schema.dump(recommendations)
        return jsonify({'items': result.data})


recommendations_api.add_resource(
    Recommendations, '/users/<string:user_pk>/recommendations'
)
