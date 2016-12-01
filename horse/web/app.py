from flask import Flask, g
from flask_cors import CORS

from .movies import movies_bp
from .recommendations import recommendations_bp
from .users import users_bp
from .populate import populate_bp


def build_web_app(ctx, name=__name__, debug=False):
    app = Flask(name)
    CORS(app)

    if debug:
        app.debug = debug

    @app.route('/')
    def hello():
        return 'Hello, world!'

    @app.before_request
    def before_request():
        g.repos = ctx.repos
        g.recommendations = ctx.recommendations

    app.register_blueprint(movies_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(populate_bp)

    return app
