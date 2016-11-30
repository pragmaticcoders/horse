from flask import Flask


def build_app(name=__name__):
    application = Flask(name)

    @application.route('/')
    def hello():
        return 'Hello, world!'

    return application
