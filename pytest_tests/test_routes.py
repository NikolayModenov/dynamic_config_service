from http import HTTPStatus

import pytest

GET_FINAL_CONFIG_URL = "get_final_config"
GET_ALL_PATCHES_URL = "get_all_patches"
DELETE_PATCH_URL = "delete_patch"
ADD_PATCH_URL = "add_patch"
UPDATE_PATCH_URL = "update_patch"
HISTORY_URL = "history"


@pytest.mark.parametrize("url, expected_status", (
    (GET_FINAL_CONFIG_URL, HTTPStatus.OK),
    (GET_ALL_PATCHES_URL, HTTPStatus.OK),
    (HISTORY_URL, HTTPStatus.OK)
))
def test_availability_get_urls(
        client, url, expected_status, good_query_parameters, good_headers
):
    assert client.get(
        url=url, params=good_query_parameters, headers=good_headers
    ).status_code == expected_status


@pytest.mark.parametrize("url, expected_status", (
    (f"/{DELETE_PATCH_URL}/2", HTTPStatus.OK),
    (f"/{DELETE_PATCH_URL}/three", HTTPStatus.UNPROCESSABLE_ENTITY),
    (f"/{DELETE_PATCH_URL}/5", HTTPStatus.NOT_FOUND),
))
def test_availability_delete_patch(
        client, url, much_patches, expected_status, good_query_parameters,
        good_headers
):
    assert client.delete(
        url=url, params=good_query_parameters, headers=good_headers
    ).status_code == expected_status


def test_availability_add_patch(
        client, test_request, good_query_parameters, good_headers
):
    assert client.post(
        ADD_PATCH_URL, json=test_request, params=good_query_parameters,
        headers=good_headers
    ).status_code == HTTPStatus.OK


@pytest.mark.parametrize("url, expected_status", (
    (f"/{UPDATE_PATCH_URL}/2", HTTPStatus.OK),
    (f"/{UPDATE_PATCH_URL}/three", HTTPStatus.UNPROCESSABLE_ENTITY),
    (f"/{UPDATE_PATCH_URL}/5", HTTPStatus.NOT_FOUND),
))
def test_availability_update_patch(
    client, patch_content, much_patches, url, expected_status,
        good_query_parameters, good_headers
):
    assert client.put(
        url, json=patch_content, params=good_query_parameters,
        headers=good_headers
    ).status_code == expected_status
