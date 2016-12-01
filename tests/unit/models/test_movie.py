from horse.models import Movie


def test_movie_defaults():
    movie = Movie('m')

    assert movie.likes == 0


def test_movie_like_added():
    movie = Movie('m')

    movie.like_added()
    assert movie.likes == 1


def test_movie_like_removed():
    movie = Movie('m')

    movie.like_added()
    assert movie.likes == 1

    movie.like_removed()
    assert movie.likes == 0


def test_movie_like_removed_when_0_likes():
    movie = Movie('m')

    assert movie.likes == 0

    movie.like_removed()
    assert movie.likes == 0
