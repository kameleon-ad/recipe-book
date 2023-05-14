from .. import app
from app.models import Aspect, Sentiment


def test_new_aspect():
    aspect = Aspect(aspect='test-aspect')
    assert aspect.aspect == 'test-aspect'


def test_all_aspect():
    with app.app_context():
        aspects = Aspect.get_all_aspects()
        assert isinstance(aspects, list)


def test_new_sentiment():
    sentiment = Sentiment(sentiment='test-sentiment')
    assert sentiment.sentiment == 'test-sentiment'


def test_all_sentiment():
    with app.app_context():
        sentiments = Sentiment.get_all_sentiments()
        assert isinstance(sentiments, list)
