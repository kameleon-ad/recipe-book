import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = db.Column(db.String(100), nullable=False)

    @staticmethod
    def get_all_tags():
        return Tag.query.all()

    @staticmethod
    def get_tag(name):
        return Tag.query.filter(Tag.name == name).first()

    @staticmethod
    def insert_tag(name):
        tag = Tag.get_tag(name)
        if tag is None:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
        return tag

    @property
    def raw(self):
        return {
            'pid': str(self.pid),
            'name': self.name,
        }

    @property
    def simple_raw(self):
        return {
            'pid': str(self.pid),
            'name': self.name,
        }
