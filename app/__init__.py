from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker

from config import BaseConfig
from app.extensions import db, cache, seeder, instances
from app.api import api


def create_app(config_class=None):
    if config_class is None:
        config_class = BaseConfig

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    cache.init_app(app)
    seeder.init_app(app, db)

    with app.app_context():
        session_factory = sessionmaker(bind=db.engine)
        session_maker = scoped_session(session_factory)
        instances['session_maker'] = session_maker
        db.create_all()

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')

    instances['app'] = app

    return app
