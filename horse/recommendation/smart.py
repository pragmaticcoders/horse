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
    base_potential = 2

    def __init__(self, user_repo, movie_repo):
        self.user_repo = user_repo
        self.movie_repo = movie_repo

    def _get_base_movie_recommendations(self, movies_to_skip):
        return [
            Recommendation(movie, 1) for movie in self.movie_repo.all()
            if movie not in movies_to_skip
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

        for other_user in relations:
            similarity = self._calculate_user_similarity_factor(
                user, other_user)
            relations[other_user] += relations[other_user] * similarity

        return relations

    def _calculate_user_similarity_factor(self, user, other):
        user_a_movies = set(user.get_liked_movies())
        user_b_movies = set(other.get_liked_movies())

        common_liked_movies_count = len(user_a_movies & user_b_movies)
        max_common_movies_count = min(len(user_a_movies), len(user_b_movies))

        if max_common_movies_count == 0:
            # Don't make any assumptions if one of the users doesn't
            # have anything rated
            return 0

        common_movies_fraction = (
            common_liked_movies_count / max_common_movies_count)

        potential = (max_common_movies_count / self.base_potential)
        potential = max(min(potential, 2), 0.5)

        return common_movies_fraction * potential

    def _increase(self, recommendations, movie, score):
        recommendation = [
            r for r in recommendations if r.movie.pk == movie.pk
        ][0]
        recommendation.score += score

    def recommend(self, user):
        movies_to_skip = user.get_liked_movies()

        recommendations = self._get_base_movie_recommendations(movies_to_skip)
        user_relations = self._get_related_users(user)

        for related_user, relation_score in user_relations.items():
            for movie in related_user.get_liked_movies():
                if movie in movies_to_skip:
                    continue

                self._increase(recommendations, movie, relation_score)

        recommendations = sorted(recommendations, key=lambda r: -r.score)

        print([(r.movie.title, r.score) for r in recommendations])

        return [r.movie for r in recommendations]
