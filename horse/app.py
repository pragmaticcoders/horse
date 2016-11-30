from horse.repositories import UserRepository, MovieRepository
from horse.web import build_web_app


class App:
    def __init__(self, web_app, ctx):
        self.web_app = web_app
        self.ctx = ctx


class AppContext:
    def __init__(self):
        self.repos = Repositories()


class Repositories:
    def __init__(self):
        self.users = UserRepository()
        self.movies = MovieRepository()


def build_app(**kwargs):
    ctx = AppContext()
    return App(
        ctx=ctx,
        web_app=build_web_app(ctx=ctx, **kwargs),
    )
