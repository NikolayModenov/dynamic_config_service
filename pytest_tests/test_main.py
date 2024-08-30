from http import HTTPStatus
import json

import pytest
from sqlalchemy import desc

from main import proto_to_dict, PROTOBUF_MESSAGE
from sql_app.crud import DELETE_COMMENT
from sql_app.models import History, Patch, OpEnum
from pytest_tests.test_routes import (
    ADD_PATCH_URL, DELETE_PATCH_URL, GET_ALL_PATCHES_URL,
    GET_FINAL_CONFIG_URL, UPDATE_PATCH_URL
)

from datetime import datetime


def test_response_empty_get_final_config(client):
    assert client.get(GET_FINAL_CONFIG_URL).json() == proto_to_dict(
        PROTOBUF_MESSAGE
    ), "the initial config does not match the protobuf"


def test_response_patched_get_final_config(
        client, much_patches, result_of_changes
):
    assert client.get(GET_FINAL_CONFIG_URL).json() == result_of_changes, (
        "an incorrect config was received"
    )


def test_response_get_all_patches(client, much_patches, patch_dicts):
    received_patches = [
        json.loads(patch['patch'])
        for patch in client.get(GET_ALL_PATCHES_URL).json()
    ]
    assert received_patches == patch_dicts, (
        "an incorrect list of patches was received"
    )


def test_logic_delete_patch(client, much_patches, test_db):
    patch_to_delete = test_db.query(Patch).get(2)
    assert patch_to_delete is not None
    json_patch = json.loads(patch_to_delete.patch)
    client.delete(f"/{DELETE_PATCH_URL}/2")
    patch_in_history = test_db.query(History).order_by(
        desc(History.id)
    ).first()
    assert patch_in_history is not None
    assert patch_in_history.operation == OpEnum.delete
    assert patch_in_history.timestamp_change == (
        datetime.utcnow().replace(microsecond=0)
    )
    assert json.loads(patch_in_history.patch) == json_patch
    assert patch_in_history.comment == DELETE_COMMENT
    assert test_db.query(Patch).get(2) is None


def test_logic_add_patch(
        client, much_patches, test_db, test_request
):
    assert test_db.query(Patch).get(4) is None
    client.post(ADD_PATCH_URL, json=test_request)
    assert test_db.query(Patch).get(4) is not None
    added_patch = test_db.query(Patch).get(4)
    patch_in_history = (
        test_db.query(History).order_by(desc(History.id)).first()
    )
    assert json.loads(added_patch.patch) == test_request["patch"]
    assert added_patch.patch == patch_in_history.patch
    assert added_patch.comment == test_request["comment"]
    assert added_patch.comment == patch_in_history.comment
    assert added_patch.timestamp_change == (
        datetime.utcnow().replace(microsecond=0)
    )
    assert added_patch.timestamp_change == patch_in_history.timestamp_change
    assert patch_in_history.operation == OpEnum.create


def test_logic_add_bad_patch(
        client, much_patches, request_with_bad_path
):
    with pytest.raises(KeyError):
        client.post(ADD_PATCH_URL, json=request_with_bad_path)


def test_availability_update_patch(
        client, much_patches, test_db, patch_content
):
    assert test_db.query(Patch).get(2) is not None
    client.put(f"/{UPDATE_PATCH_URL}/2", json=patch_content)
    new_patch = test_db.query(Patch).get(2)
    patch_in_history = (
        test_db.query(History).order_by(desc(History.id)).first()
    )
    assert json.loads(new_patch.patch) == patch_content["patch"]
    assert new_patch.patch == patch_in_history.patch
    assert new_patch.comment == patch_content["comment"]
    assert new_patch.comment == patch_in_history.comment
    assert new_patch.timestamp_change == (
        datetime.utcnow().replace(microsecond=0)
    )
    assert new_patch.timestamp_change == patch_in_history.timestamp_change
    assert patch_in_history.operation == OpEnum.update
