import uuid
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db
from app.models import RecipeTag, Tag


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text())
    instructions = db.Column(db.Text())
    cook_time = db.Column(db.Integer, default=0)
    tags = db.relationship('Tag', secondary=RecipeTag.__table__,
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
            return RecipeTag.update(self.pid, old_tag.pid, new_tag.pid)
        return RecipeTag.insert(self.pid, new_tag.pid)

    def set(self, data):
        if 'title' in data:
            self.title = data['title']
        if 'ingredients' in data:
            self.ingredients = data['ingredients']
        if 'instructions' in data:
            self.instructions = data['instructions']
        if 'cook_time' in data:
            self.cook_time = data['cook_time']
        if 'tags' in data:
            for tag in self.tags:
                self.set_tag(tag)
        db.session.commit()

    @staticmethod
    def get_all_recipes():
        return Recipe.query.all()

    @staticmethod
    def get_recipe(recipe_pid):
        return Recipe.query.filter(Recipe.pid == recipe_pid).first()

    @staticmethod
    def add_new_recipe(data):
        new_recipe = Recipe(**data)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    @property
    def raw(self):
        return {'pid': str(self.pid), 'text': self.text, 'tags': [tag.simple_raw for tag in self.tags]}

    @staticmethod
    def all():
        return [recipe.raw for recipe in Recipe.get_all_recipes()]
