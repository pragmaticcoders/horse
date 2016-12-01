from horse.models import Recommendation
from .base import RecommendationService


class DummyRecommendationService(RecommendationService):
    def recommend(self, user):
        result = []
        for followed_user in user.get_followed_users():
            for movie in followed_user.get_liked_movies():
                result.append(Recommendation(movie=movie, weight=1))
        return result
