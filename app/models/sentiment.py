import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Sentiment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    sentiment = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_all_sentiments():
        return Sentiment.query.all()

    @staticmethod
    def add_new_sentiment(sentiment: str):
        new_sentiment = Sentiment(sentiment=sentiment)
        db.session.add(new_sentiment)
        db.session.commit()
        return new_sentiment

    @property
    def raw(self):
        return {'pid': str(self.pid), 'sentiment': self.sentiment}
