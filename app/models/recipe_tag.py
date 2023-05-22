from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class recipeTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_pid = db.Column(UUID, db.ForeignKey('recipe.pid'), nullable=False)
    tag_pid = db.Column(UUID, db.ForeignKey('tag.pid'), nullable=False)

    @staticmethod
    def get(recipe_pid, tag_pid):
        recipe_pid, tag_pid = str(recipe_pid), str(tag_pid)
        return recipeTag.query\
            .filter(and_(recipeTag.recipe_pid == recipe_pid, recipeTag.tag_pid == tag_pid)).first()

    @staticmethod
    def insert(recipe_pid, tag_pid):
        recipe_pid, tag_pid = str(recipe_pid), str(tag_pid)

        recipe_tag = recipeTag.get(recipe_pid, tag_pid)

        if recipe_tag is None:
            recipe_tag = recipeTag(recipe_pid=recipe_pid, tag_pid=tag_pid)
            db.session.add(recipe_tag)
            db.session.commit()

        return recipe_tag

    @staticmethod
    def update(recipe_pid, old_tag_pid, new_tag_pid):
        recipe_pid, old_tag_pid, new_tag_pid = str(recipe_pid), str(old_tag_pid), str(new_tag_pid)
        recipe_tag: recipeTag = recipeTag.get(recipe_pid, old_tag_pid)
        recipe_tag.tag_pid = new_tag_pid
        db.session.commit()
        return recipe_tag

    @property
    def raw(self):
        return {'recipe_pid': str(self.recipe_pid)}
