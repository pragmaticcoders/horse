from flask import Flask

from .movies import movies_bp


def build_app(name=__name__):
    app = Flask(name)

    @app.route('/')
    def hello():
        return 'Hello, world!'

    app.register_blueprint(movies_bp)

    return app
