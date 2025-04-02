from flask import Flask
from web.config import Config
from web.auth import OAuthHandler
from web.views import views


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["oauth_providers"] = {}

    for provider in Config.OAUTH_PROVIDERS:
        oauth_instance = OAuthHandler(app, provider, Config)
        app.config["oauth_providers"][provider]: OAuthHandler = oauth_instance
        print([provider])

    app.register_blueprint(views)

    return app

