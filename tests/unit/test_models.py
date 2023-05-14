from sqlalchemy.dialects.postgresql import UUID

from .. import app
from app.extensions import db
from app.models import Aspect, Sentiment, Tag


def test_new_aspect():
    aspect = Aspect(aspect='test-new-aspect')
    assert aspect.aspect == 'test-new-aspect'


def test_all_aspect():
    with app.app_context():
        aspects = Aspect.get_all_aspects()
        assert isinstance(aspects, list)


def test_new_sentiment():
    sentiment = Sentiment(sentiment='test-new-sentiment')
    assert sentiment.sentiment == 'test-new-sentiment'


def test_all_sentiment():
    with app.app_context():
        sentiments = Sentiment.get_all_sentiments()
        assert isinstance(sentiments, list)


def test_new_tag():
    aspect = Aspect(aspect='test-new-tag-aspect')
    sentiment = Sentiment(sentiment='test-new-tag-sentiment')

    with app.app_context():
        db.session.add(aspect)
        db.session.add(sentiment)
        db.session.commit()
        db.session.refresh(aspect)
        db.session.refresh(sentiment)

    tag = Tag(aspect_pid=aspect.pid, sentiment_pid=sentiment.pid)

    with app.app_context():
        db.session.add(tag)
        db.session.commit()
        db.session.refresh(tag)
        db.session.refresh(tag.aspect)
        db.session.refresh(tag.sentiment)

    assert tag.aspect.aspect == aspect.aspect
    assert tag.sentiment.sentiment == sentiment.sentiment
    assert tag.aspect.pid == aspect.pid
    assert tag.sentiment.pid == sentiment.pid
