from flask import Flask


def build_app(name=__name__):
    app = Flask(name)

    @app.route('/')
    def hello():
        return 'Hello, world!'

    return app
