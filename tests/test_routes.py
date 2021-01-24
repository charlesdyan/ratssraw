import pytest
import ratssraw

@pytest.fixture
def client():
    app = ratssraw.create_app()
    return app.test_client()


def test_films_route(client):
    assert client.get('/films').status_code == 200


@pytest.mark.parametrize(('json', 'expected_status'), (
    ({'filmID': 1}, 200),
    ({'filmID': 10}, 500),
    ({}, 400),
    ({'unexpected_data': '?'}, 400)
))
def test_characters_route(client, json, expected_status):
    assert client.post('/characters', json=json).status_code == expected_status