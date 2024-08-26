import json
from typing import Dict

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from validators import validate_patch_with_proto

from proto import example_pb2
from sql_app import crud
from sql_app.database import get_db


APP = FastAPI()

DATABASE_SESSION = Depends(get_db)

PROTOBUF_MESSAGE = example_pb2.ServiceConfig()


def proto_to_dict(proto):
    new_dict = {}
    for field in proto.DESCRIPTOR.fields:
        field_val = getattr(proto, field.name)
        if field.type == field.TYPE_MESSAGE:
            new_dict[field.name] = proto_to_dict(field_val)
            if not new_dict[field.name]:
                new_dict.pop(field.name)
        elif proto.HasField(field.name) or field.has_default_value:
            new_dict[field.name] = field_val
    if new_dict:
        return new_dict
    return None


def patching_config(config, patch):
    for key in patch:
        if type(patch[key]) is dict:
            config[key] = patching_config(config[key], patch[key])
        else:
            config[key] = patch[key]
    return config


@APP.get("/get_final_config")
def get_final_config(db: Session = DATABASE_SESSION):
    config = proto_to_dict(PROTOBUF_MESSAGE)
    for patch_object in crud.get_patches(db):
        patch = json.loads(patch_object.patch)
        config = patching_config(config, patch)
    return config


@APP.get("/get_all_patches")
def get_all_patches(db: Session = DATABASE_SESSION):
    return crud.get_patches(db)


@APP.delete("/delete_patch/{patch_id}")
def delete_patch(patch_id: int, db: Session = DATABASE_SESSION):
    return crud.del_patches(db, patch_id)


@APP.post("/add_patch")
def add_patch(patch: Dict, db: Session = DATABASE_SESSION):
    validate_patch_with_proto(patch, PROTOBUF_MESSAGE)
    jsoned_patch = json.dumps(patch)
    return crud.create_patch(db, jsoned_patch)


@APP.put("/update_patch/{patch_id}")
def update_patch(patch: Dict, patch_id: int, db: Session = DATABASE_SESSION):
    validate_patch_with_proto(patch, PROTOBUF_MESSAGE)
    jsoned_patch = json.dumps(patch)
    return crud.put_patches(db, patch_id, jsoned_patch)
