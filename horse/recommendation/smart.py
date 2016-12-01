from collections import defaultdict
from .base import RecommendationService


class Recommendation:
    def __init__(self, movie, score):
        self.movie = movie
        self.score = score

    def __repr__(self):
        return 'Recommendation({}, {})'.format(self.movie, self.score)


class Relation:
    def __init__(self, user, score):
        self.user = user
        self.score = score


class SmartRecommendationService(RecommendationService):
    def __init__(self, user_repo, movie_repo):
        self.user_repo = user_repo
        self.movie_repo = movie_repo

    def _get_base_movie_recommendations(self):
        return [
            Recommendation(movie, 1) for movie in self.movie_repo.all()
        ]

    def _get_related_users(self, user):
        relations = defaultdict(int)

        def recur(root_user, power, depth=0):
            if depth > 3:
                return

            for followed in root_user.get_followed_users():
                relations[followed] += power
                recur(followed, power / 2, depth + 1)

        recur(user, 1)

        return relations

    def _increase(self, recommendations, movie, score):
        recommendation = [
            r for r in recommendations if r.movie.pk == movie.pk
        ][0]
        recommendation.score += score

    def recommend(self, user):
        recommendations = self._get_base_movie_recommendations()
        user_relations = self._get_related_users(user)

        for related_user, relation_score in user_relations.items():
            for movie in related_user.get_liked_movies():
                self._increase(recommendations, movie, relation_score)

        recommendations = sorted(recommendations, key=lambda r: -r.score)

        print([(r.movie.title, r.score) for r in recommendations])

        return [r.movie for r in recommendations]
