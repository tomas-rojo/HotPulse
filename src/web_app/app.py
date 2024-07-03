import os

from flask import Flask

from config.environment import Environment
from web_app.blueprints import api

app = Flask(__name__)


def create_app() -> Flask:  # noqa
    os.environ["APP_ENVIRONMENT"] = "development"
    Environment.bootstrap()
    app.register_blueprint(api.bp)
    return app
