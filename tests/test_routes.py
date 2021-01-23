import pytest

from ratssraw import ratssraw

@pytest.fixture
def client():
    ratssraw.app.config['TESTING'] = True
    return ratssraw.app.test_client()
