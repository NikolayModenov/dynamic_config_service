from http import HTTPStatus

import pytest


@pytest.mark.parametrize("url, expected_status", (
    ("get_final_config", HTTPStatus.OK),
    ("get_all_patches", HTTPStatus.OK),
))
def test_pages_availability(default_client, url, expected_status):
    assert default_client.get(url).status_code == expected_status
