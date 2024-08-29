from http import HTTPStatus

import pytest

GET_FINAL_CONFIG_URL = "get_final_config"
GET_ALL_PATCHES_URL = "get_all_patches"
DELETE_PATCH_URL = "delete_patch"
ADD_PATCH_URL = "add_patch"
UPDATE_PATCH_URL = "update_patch"


def test_availability_get_final_config(client):
    assert client.get(GET_FINAL_CONFIG_URL).status_code == HTTPStatus.OK


def test_availability_get_all_patches(client):
    assert client.get(GET_ALL_PATCHES_URL).status_code == HTTPStatus.OK


@pytest.mark.parametrize("url, expected_status", (
    (f"/{DELETE_PATCH_URL}/2", HTTPStatus.OK),
    (f"/{DELETE_PATCH_URL}/three", HTTPStatus.UNPROCESSABLE_ENTITY),
    (f"/{DELETE_PATCH_URL}/5", HTTPStatus.NOT_FOUND),
))
def test_availability_delete_patch(client, url, much_patches, expected_status):
    assert client.delete(url).status_code == expected_status


def test_availability_add_patch(client, dict_for_the_post_request):
    assert client.post(
        ADD_PATCH_URL, json=dict_for_the_post_request
    ).status_code == HTTPStatus.OK


@pytest.mark.parametrize("url, expected_status", (
    (f"/{UPDATE_PATCH_URL}/2", HTTPStatus.OK),
    (f"/{UPDATE_PATCH_URL}/three", HTTPStatus.UNPROCESSABLE_ENTITY),
    (f"/{UPDATE_PATCH_URL}/5", HTTPStatus.NOT_FOUND),
))
def test_availability_update_patch(
    client, patch_content, much_patches, url, expected_status
):
    assert client.put(url, json=patch_content).status_code == expected_status
