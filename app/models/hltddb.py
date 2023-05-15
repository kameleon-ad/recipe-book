# HLTDDB: Human Level Text and Document - Database
import uuid
from datetime import datetime
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db
from app.models import HltddbTag, Tag


class Hltddb(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=HltddbTag.__table__,
                           backref=backref('Hltddb'),
                           cascade='save-update, merge, delete')

    def get_tag(self, aspect_pid):
        for tag in self.tags:
            if tag.aspect_pid == aspect_pid:
                return tag
        return None

    def get_sentiment(self, aspect_pid):
        tag = self.get_tag(aspect_pid)
        if tag is None:
            return None
        return tag.sentiment

    def set_sentiment(self, aspect_pid, sentiment_pid):

        aspect_pid, sentiment_pid = str(aspect_pid), str(sentiment_pid)

        old_tag = self.get_tag(aspect_pid)
        new_tag = Tag.insert_tag(aspect_pid, sentiment_pid)

        if old_tag is not None:
            return HltddbTag.update(self.pid, old_tag.pid, new_tag.pid)
        return HltddbTag.insert(self.pid, new_tag.pid)

    @staticmethod
    def get_all_hltddbs():
        return Hltddb.query.all()

    @staticmethod
    def get_hltddb(hltddb_pid):
        return Hltddb.query.filter(Hltddb.pid == hltddb_pid).first()

    @staticmethod
    def add_new_hltddb(text):
        new_hltddb = Hltddb(text=text)
        db.session.add(new_hltddb)
        db.session.commit()
        return new_hltddb

    @property
    def raw(self):
        return {'pid': str(self.pid), 'text': self.text, 'tags': [tag.simple_raw for tag in self.tags]}

    @staticmethod
    def all():
        return [hltddb.raw for hltddb in Hltddb.get_all_hltddbs()]
