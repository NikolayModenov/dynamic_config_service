from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from sql_app.models import OpEnum
from . import models


DELETE_COMMENT = "delete patch"


def validate_comment_in_crud(comment):
    if not comment:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Comment not found"
        )


def validate_patch_in_crud(patch):
    if not patch:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Patch not found"
        )


def add_patch_to_history(db, patch, operation, comment, user, service, stage):
    db_history_patch = models.History(
        patch=patch, operation=operation, comment=comment, user=user,
        service=service, stage=stage
    )
    db.add(db_history_patch)
    db.commit()
    db.refresh(db_history_patch)


def get_patches(db: Session, service, stage, user):
    return db.query(models.Patch).filter_by(
        service=service, stage=stage, user=user
    ).all()


def create_patch(
        db: Session, patch: str, comment: str, user: str, service: str,
        stage: str
):
    validate_comment_in_crud(comment)
    db_patch = models.Patch(
        patch=patch, comment=comment, user=user, service=service, stage=stage
    )
    db.add(db_patch)
    add_patch_to_history(
        db, patch, OpEnum.create, comment=comment, user=user, service=service,
        stage=stage
    )
    db.commit()
    db.refresh(db_patch)
    return db_patch


def del_patches(db: Session, patch_id: int, user: str):
    db_patch = db.get(models.Patch, patch_id)
    if not db_patch:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Patch with id {patch_id} not found"
        )
    validate_patch_in_crud(db_patch)
    add_patch_to_history(
        db, db_patch.patch, OpEnum.delete, comment=DELETE_COMMENT,
        user=user, service=db_patch.service, stage=db_patch.stage
    )
    db.delete(db_patch)
    db.commit()
    return {"message": "Patch deleted successfully"}


def put_patches(
        db: Session, patch_id: int, patch: str, comment: str, user: str
):
    validate_comment_in_crud(comment)
    db_patch = db.get(models.Patch, patch_id)
    if not db_patch:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Patch with id {patch_id} not found"
        )
    validate_patch_in_crud(db_patch)
    db_patch.patch = patch
    db_patch.timestamp_change = datetime.utcnow().replace(microsecond=0)
    db_patch.comment = comment
    add_patch_to_history(
        db, patch, OpEnum.update, comment, user=user, service=db_patch.service,
        stage=db_patch.stage
    )
    db.commit()
    db.refresh(db_patch)
    return db_patch


def get_history_of_changes(db: Session, service: str, stage: str):
    return db.query(models.History).filter_by(service=service, stage=stage)
