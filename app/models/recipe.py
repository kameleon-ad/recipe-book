import uuid
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db
from app.models import recipeTag, Tag


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text())
    instructions = db.Column(db.Text())
    cook_time = db.Column(db.Integer, default=0)
    tags = db.relationship('Tag', secondary=recipeTag.__table__,
                           backref=backref('Recipe'),
                           cascade='save-update, merge, delete')

    def get_tag(self, tag_pid):
        for tag in self.tags:
            if tag.pid == tag_pid:
                return tag
        return None

    def set_tag(self, tag_name):
        new_tag = Tag.insert_tag(tag_name)

        tag_pid = str(new_tag.pid)
        old_tag = self.get_tag(tag_pid)

        if old_tag is not None:
            return recipeTag.update(self.pid, old_tag.pid, new_tag.pid)
        return recipeTag.insert(self.pid, new_tag.pid)

    @staticmethod
    def get_all_recipes():
        return Recipe.query.all()

    @staticmethod
    def get_recipe(recipe_pid):
        return Recipe.query.filter(Recipe.pid == recipe_pid).first()

    @staticmethod
    def add_new_recipe(text):
        new_recipe = Recipe(text=text)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    @property
    def raw(self):
        return {'pid': str(self.pid), 'text': self.text, 'tags': [tag.simple_raw for tag in self.tags]}

    @staticmethod
    def all():
        return [recipe.raw for recipe in Recipe.get_all_recipes()]
