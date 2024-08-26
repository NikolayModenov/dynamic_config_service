

def test_get_final_config(client):
    assert client.get('get_final_config').json() == {
        'port': 8080, 'service': {'timeout_ms': 100}
    }
