from .base import RecommendationService


class DummyRecommendationService(RecommendationService):
    def recommend(self, user):
        result = []
        for followed_user in user.get_followed_users():
            result.extend(followed_user.get_liked_movies())
        return result
