from flask import Flask

from config import BaseConfig
from app.extensions import db, cache, instances
from app.api import api


def create_app(config_class=None):
    if config_class is None:
        config_class = BaseConfig

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    cache.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')

    instances['app'] = app

    return app
