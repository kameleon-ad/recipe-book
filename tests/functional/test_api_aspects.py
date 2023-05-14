from . import test_client


def test_api_aspects():
    response = test_client.get('/api/aspects', follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert type(response.json) == list


def test_api_new_aspect():
    response = test_client.post('/api/aspects', data={'aspect': 'test-new-aspect-api'}, follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert 'aspect' in response.json
    assert 'pid' in response.json
