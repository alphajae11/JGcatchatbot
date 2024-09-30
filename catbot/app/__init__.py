from flask import Flask
from .routes import bp
from .config import Config


def create_app():
    application = Flask(__name__)
    application.config.from_object(Config)
    application.register_blueprint(bp)
    return application
