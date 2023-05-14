from . import test_client


def test_api_tags():
    response = test_client.get('/api/tags', follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert type(response.json) == list


def test_api_insert_tag():
    tag_info = {
        'aspect': 'test-insert-new-tag-aspect',
        'sentiment': 'test-insert-new-tag-sentiment',
    }

    aspect = test_client.post('/api/aspects', data=tag_info, follow_redirects=True).json
    sentiment = test_client.post('/api/sentiments', data=tag_info, follow_redirects=True).json
    response = test_client.post('/api/tags', data={'aspect': aspect['pid'], 'sentiment': sentiment['pid']},
                                follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert 'aspect' in response.json
    assert 'aspect' in response.json['aspect']
    assert response.json['aspect']['aspect'] == tag_info['aspect']
    assert 'sentiment' in response.json
    assert 'sentiment' in response.json['sentiment']
    assert response.json['sentiment']['sentiment'] == tag_info['sentiment']
    assert 'pid' in response.json
