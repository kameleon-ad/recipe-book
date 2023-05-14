from . import test_client


def test_home_page():
    response = test_client.get('/api/test')
    assert response.status_code == 200
    assert b'working' in response.data
