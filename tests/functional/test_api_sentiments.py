from . import test_client


def test_api_sentiments():
    response = test_client.get('/api/sentiments', follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert type(response.json) == list


def test_api_new_sentiment():
    response = test_client.post('/api/sentiments', data={"sentiment": "test-sentiment"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert 'sentiment' in response.json
    assert 'pid' in response.json
