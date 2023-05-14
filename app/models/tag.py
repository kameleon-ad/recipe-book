import uuid
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    aspect_pid = db.Column(UUID, db.ForeignKey('aspect.pid'), nullable=False)
    sentiment_pid = db.Column(UUID, db.ForeignKey('sentiment.pid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    aspect = db.relationship('Aspect', backref=backref('tag', lazy=True))
    sentiment = db.relationship('Sentiment', backref=backref('tag', lazy=True))

    def __init__(self, aspect_pid, sentiment_pid, **kwargs):
        super().__init__(aspect_pid=str(aspect_pid), sentiment_pid=str(sentiment_pid), **kwargs)

    @staticmethod
    def get_all_tags():
        return Tag.query.all()

    @staticmethod
    def get_tag(aspect, sentiment):
        return Tag.query.filter(and_(Tag.aspect_pid == aspect, Tag.sentiment_pid == sentiment)).first()

    @staticmethod
    def insert_tag(aspect_pid, sentiment_pid):

        aspect_pid, sentiment_pid = str(aspect_pid), str(sentiment_pid)

        tag = Tag.get_tag(aspect_pid, sentiment_pid)
        if tag is None:
            tag = Tag(aspect_pid=aspect_pid, sentiment_pid=sentiment_pid)
            db.session.add(tag)
            db.session.commit()
        return tag

    @property
    def raw(self):
        return {
            'pid': str(self.pid),
            'aspect': self.aspect.raw,
            'sentiment': self.sentiment.raw
        }

    @property
    def simple_raw(self):
        return {
            'pid': str(self.pid),
            'aspect': self.aspect.aspect,
            'sentiment': self.sentiment.sentiment
        }
