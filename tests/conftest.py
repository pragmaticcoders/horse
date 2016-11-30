import pytest

from horse import app


@pytest.fixture
def client():
    client = app.test_client()
    client.testing = True
    return client
