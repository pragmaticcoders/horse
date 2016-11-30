from flask import Flask

from .movies import movies_bp
from .users import users_bp


def build_app(name=__name__):
    app = Flask(name)

    @app.route('/')
    def hello():
        return 'Hello, world!'

    app.register_blueprint(movies_bp)
    app.register_blueprint(users_bp)

    return app
