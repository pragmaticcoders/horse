class User:
    def __init__(self, name, followed_users=None, liked_movies=None):
        self.name = name
        self._followed_users = followed_users or []
        self._liked_movies = liked_movies or []

    def get_followed_users(self):
        return list(self._followed_users)

    def add_to_followed_users(self, user):
        self._followed_users.append(user)

    def get_liked_movies(self):
        return list(self._liked_movies)

    def add_to_liked_movies(self, movie):
        self._liked_movies.append(movie)

        movie.like_added()
