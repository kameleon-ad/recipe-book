from .. import app
from app.models import Aspect


def test_new_aspect():
    aspect = Aspect(aspect='test-aspect')
    assert aspect.aspect == 'test-aspect'


def test_all_aspect():
    with app.app_context():
        aspects = Aspect.get_all_aspects()
        assert isinstance(aspects, list)
