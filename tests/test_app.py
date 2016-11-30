def test_hello(client):
    result = client.get('/')
    assert result.data == b'Hello, world!'
