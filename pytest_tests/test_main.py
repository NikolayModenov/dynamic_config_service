

def test_get_final_config(default_client):
    assert default_client.get('get_final_config').json() == {
        'port': 8080, 'service': {'timeout_ms': 100}
    }


def test_add_patch(default_client, json_for_the_post_request):
    response = default_client.post(
        'get_final_config', json=json_for_the_post_request
    )
    assert response.status_code == 200
    # assert response.json() ==
