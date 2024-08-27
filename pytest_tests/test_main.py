from http import HTTPStatus
import json

import pytest

from main import proto_to_dict, PROTOBUF_MESSAGE
from sql_app.models import Patch


GET_FINAL_CONFIG_URL = "get_final_config"


def test_availability_get_final_config(client):
    assert client.get(GET_FINAL_CONFIG_URL).status_code == HTTPStatus.OK


def test_response_empty_get_final_config(client):
    assert client.get(GET_FINAL_CONFIG_URL).json() == proto_to_dict(
        PROTOBUF_MESSAGE
    ), "the initial config does not match the protobuf"


def test_response_patched_get_final_config(client, much_patches):
    result = {
        "monitoring_url": "",
        "port": 8081,
        "service": {
            "timeout_ms": 212
        }
    }
    assert client.get(GET_FINAL_CONFIG_URL).json() == result, (
        "an incorrect config was received"
    )


def test_availability_get_all_patches(client, much_patches):
    assert client.get("get_all_patches").status_code == HTTPStatus.OK


def test_response_get_all_patches(client, much_patches, patch_dicts):
    received_patches = [
        json.loads(patch['patch'])
        for patch in client.get("get_all_patches").json()
    ]
    assert received_patches == patch_dicts, (
        "an incorrect list of patches was received"
    )


@pytest.mark.parametrize("url, expected_status", (
    ("/delete_patch/2", HTTPStatus.OK),
    ("/delete_patch/three", HTTPStatus.UNPROCESSABLE_ENTITY),
    ("/delete_patch/5", HTTPStatus.NOT_FOUND),
))
def test_availability_delete_patch(client, much_patches, url, expected_status):
    assert client.delete(url).status_code == expected_status


def test_logic_delete_patch(client, much_patches, test_db):
    assert test_db.query(Patch).get(2) is not None
    client.delete("/delete_patch/2")
    assert test_db.query(Patch).get(2) is None


def test_logic_add_patch(
        client, much_patches, test_db, dict_for_the_post_request
):
    assert test_db.query(Patch).get(4) is None
    client.post("add_patch", json=dict_for_the_post_request)
    assert test_db.query(Patch).get(4) is not None


def test_logic_add_bad_patch(
        client, much_patches, bad_dict_for_the_post_request
):
    with pytest.raises(KeyError):
        client.post("add_patch", json=bad_dict_for_the_post_request)


def test_availability_update_patch(client, much_patches, test_db):
    patch_content = {"monitoring_url": "https://new.com"}
    old_patch = test_db.query(Patch).get(2)
    assert old_patch is not None
    old_json_patch = json.loads(old_patch.patch)
    assert old_json_patch != patch_content
    response = client.put("/update_patch/2", json=patch_content)
    assert response.status_code == HTTPStatus.OK
    new_patch = test_db.query(Patch).get(2)
    assert new_patch is not None
    new_json_patch = json.loads(new_patch.patch)
    assert new_json_patch == patch_content

