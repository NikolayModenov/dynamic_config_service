from http import HTTPStatus
import json

import pytest
from sqlalchemy import desc

from main import proto_to_dict, PROTOBUF_MESSAGE
from sql_app.models import History, Patch


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


def test_response_get_all_patches(client, much_patches, patch_dicts):
    received_patches = [
        json.loads(patch['patch'])
        for patch in client.get("get_all_patches").json()
    ]
    assert received_patches == patch_dicts, (
        "an incorrect list of patches was received"
    )


def test_logic_delete_patch(client, much_patches, test_db):
    patch_to_delete = test_db.query(Patch).get(2)
    assert patch_to_delete is not None
    json_patch = json.loads(patch_to_delete.patch)
    last_patch_in_history_before_deleting = test_db.query(History).order_by(
        desc(History.id)
    ).first()
    if last_patch_in_history_before_deleting is not None:
        assert json_patch != json.loads(
            last_patch_in_history_before_deleting.patch
        )
    client.delete("/delete_patch/2")
    history_operation_after_deleting = test_db.query(History).order_by(
        desc(History.id)
    ).first()
    assert history_operation_after_deleting is not None
    assert json_patch == json.loads(history_operation_after_deleting.patch)
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


def test_availability_update_patch(
        client, much_patches, test_db, patch_content
    ):
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
