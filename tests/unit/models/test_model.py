from horse.models import Movie


def test_movie():
    movie = Movie('m')

    assert movie.likes == 0


def test_movie_like_added():
    movie = Movie('m')

    movie.like_added()
    assert movie.likes == 1
