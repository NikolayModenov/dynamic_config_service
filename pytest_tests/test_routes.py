from http import HTTPStatus

import pytest


@pytest.mark.parametrize("url, expected_status", (
    ("get_final_config", HTTPStatus.OK),
    ("get_all_patches", HTTPStatus.OK),
))
def test_pages_availability(client, url, expected_status):
    assert client.get(url).status_code == expected_status
