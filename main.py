import json
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException, Request
from google.protobuf.json_format import ParseDict
from sqlalchemy.orm import Session

from base_configs.operations import (
    get_patch_schema, get_initial_config, get_name_project_file
)
from sql_app import crud, schemas
from sql_app.database import get_db

APP = FastAPI()

DATABASE_SESSION = Depends(get_db)


def patching_config(config, patch):
    for key in patch:
        if type(patch[key]) is dict:
            config[key] = patching_config(config[key], patch[key])
        else:
            config[key] = patch[key]
    return config


@APP.get("/get_final_config")
def get_final_config(
        request: Request, service: str, stage: str,
        db: Session = DATABASE_SESSION
):
    name_project_file = get_name_project_file(service, stage)
    if not request.headers.get('username'):
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail="Username not found"
        )
    config = get_initial_config(name_project_file)
    user = request.headers.get('username')
    for patch_object in crud.get_patches(db, service, stage, user):
        patch = json.loads(patch_object.patch)
        config = patching_config(config, patch)
    return config


@APP.get("/get_all_patches")
def get_all_patches(
        request: Request, service: str, stage: str,
        db: Session = DATABASE_SESSION
):
    get_name_project_file(service, stage)
    if not request.headers.get('username'):
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail="Username not found"
        )
    user = request.headers.get('username')
    return crud.get_patches(db, service, stage, user)


@APP.delete("/delete_patch/{patch_id}")
def delete_patch(
    patch_id: int, request: Request,
    db: Session = DATABASE_SESSION
):
    if not request.headers.get('username'):
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail="Username not found"
        )
    user = request.headers.get('username')
    return crud.del_patches(db, patch_id, user)


@APP.post("/add_patch")
def add_patch(
        request: Request, service: str, stage: str, patch: schemas.Patch,
        db: Session = DATABASE_SESSION
):
    project_name = get_name_project_file(service, stage)
    if not request.headers.get('username'):
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail="Username not found"
        )
    protobuf = get_patch_schema(project_name)
    ParseDict(patch.patch, protobuf())
    comment = patch.comment
    jsoned_patch = json.dumps(patch.patch)
    user = request.headers.get('username')
    return crud.create_patch(db, jsoned_patch, comment, user, service, stage)


@APP.put("/update_patch/{patch_id}")
def update_patch(
        patch: schemas.Patch, patch_id: int, request: Request, service: str,
        stage: str, db: Session = DATABASE_SESSION
):
    project_name = get_name_project_file(service, stage)
    if not request.headers.get('username'):
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail="Username not found"
        )
    protobuf = get_patch_schema(project_name)
    ParseDict(patch.patch, protobuf())
    comment = patch.comment
    jsoned_patch = json.dumps(patch.patch)
    user = request.headers.get('username')
    return crud.put_patches(db, patch_id, jsoned_patch, comment, user)


@APP.get("/history")
def get_history(
        request: Request, service: str, stage: str,
        db: Session = DATABASE_SESSION
):
    if not request.headers.get('username'):
        get_name_project_file(service, stage)
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail="Username not found"
        )
    return crud.get_history_of_changes(db, service, stage)
