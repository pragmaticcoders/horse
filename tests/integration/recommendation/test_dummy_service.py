from horse.recommendation.dummy_service import DummyRecommendationService


def test_recommendation_for_user_with_one_followed(user, followed_user, movie):
    followed_user.add_to_liked_movies(movie)

    user.add_to_followed_users(followed_user)

    service = DummyRecommendationService()
    result = service.recommend(user)

    assert len(result) == 1
    assert movie in result
