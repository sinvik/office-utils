from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from web.config import Config
from web.auth import OAuthHandler
from web.views import views


def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    app.config.from_object(Config)

    app.config["oauth_providers"] = {}

    for provider in Config.OAUTH_PROVIDERS:
        oauth_instance = OAuthHandler(app, provider, Config)
        app.config["oauth_providers"][provider]: OAuthHandler = oauth_instance
        print([provider])

    app.register_blueprint(views)

    return app


def connect_db(app):
    from back_end.mongo_connector import MongoDBConnector

    conn = MongoDBConnector(app.config["MONGO_URL"])
    # app.config["mongo_db"] = conn.load_database(app.config["MONGO_DB"])
