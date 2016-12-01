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
        for user in user.get_followed_users():
            yield Relation(user, 1)

    def _increase(self, recommendations, movie, score):
        recommendation = [
            r for r in recommendations if r.movie.pk == movie.pk
        ][0]
        recommendation.score += score

    def recommend(self, user):
        recommendations = self._get_base_movie_recommendations()
        user_relations = self._get_related_users(user)

        for relation in user_relations:
            for movie in relation.user.get_liked_movies():
                self._increase(recommendations, movie, relation.score)

        recommendations = sorted(recommendations, key=lambda r: -r.score)

        print([(r.movie.title, r.score) for r in recommendations])

        return [r.movie for r in recommendations]
