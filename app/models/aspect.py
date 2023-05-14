import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app import db


class Aspect(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    aspect = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_all_aspects():
        return Aspect.query.all()

    @staticmethod
    def add_new_aspect(aspect: str):
        new_aspect = Aspect(aspect=aspect)
        db.session.add(new_aspect)
        db.session.commit()
        return new_aspect

    @property
    def raw(self):
        return {'pid': str(self.pid), 'aspect': self.aspect}
