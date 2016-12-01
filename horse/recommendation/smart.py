from collections import defaultdict

from .base import RecommendationService


class SmartRecommendationService(RecommendationService):
    def __init__(self,
                 user_repo,
                 movie_repo,
                 user_common_movies_threshold=2,
                 movie_likes_fraction_exp=0.5,
                 max_relation_depth=3,
                 base_relation_power=1,
                 relation_level_divisor=2,
                 max_relationship_significance=2,
                 min_relationship_significance=0.5):

        self.user_repo = user_repo
        self.movie_repo = movie_repo
        self.user_common_movies_threshold = user_common_movies_threshold
        self.movie_likes_fraction_exp = movie_likes_fraction_exp
        self.max_relation_depth = max_relation_depth
        self.base_relation_power = base_relation_power
        self.relation_level_divisor = relation_level_divisor
        self.max_relationship_significance = max_relationship_significance
        self.min_relationship_significance = min_relationship_significance

    def recommend(self, user):
        movies_to_skip = user.get_liked_movies()
        recommendations = self._get_base_movie_recommendations(movies_to_skip)
        user_relations = self._get_related_users(user)
        self._add_relations_scores(
            movies_to_skip, recommendations, user_relations)

        items = sorted(recommendations.items(), key=lambda i: -i[1])

        return [item[0] for item in items]

    def _get_base_movie_recommendations(self, movies_to_skip):
        all_movies = self.movie_repo.all()
        most_likes = max([m.likes for m in all_movies])

        if not most_likes:
            return []

        def calc_movie_score(movie):
            return (movie.likes / most_likes) ** self.movie_likes_fraction_exp

        movie_scores = {}

        for movie in set(all_movies) - set(movies_to_skip):
            score = calc_movie_score(movie)
            if score:
                movie_scores[movie] = score

        return movie_scores

    def _get_related_users(self, user):
        relations = defaultdict(int)

        def recur(root_user, power, depth=0):
            if depth > self.max_relation_depth:
                return

            for followed in root_user.get_followed_users():
                relations[followed] += power
                next_power = power / self.relation_level_divisor
                recur(followed, next_power, depth + 1)

        recur(user, self.base_relation_power)

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

        significance = (max_common_movies_count /
                        self.user_common_movies_threshold)
        significance = max(significance, self.min_relationship_significance)
        significance = min(significance, self.max_relationship_significance)

        return common_movies_fraction * significance

    def _add_relations_scores(
            self, movies_to_skip, recommendations, user_relations):

        for related_user, relation_score in user_relations.items():
            for movie in related_user.get_liked_movies():
                if movie in movies_to_skip:
                    continue

                recommendations[movie] += relation_score
