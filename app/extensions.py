from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_seeder import FlaskSeeder


db = SQLAlchemy()
cache = Cache()
seeder = FlaskSeeder()
instances = {}
