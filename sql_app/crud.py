from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from sql_app.models import OpEnum
from . import models


def validate_comment_in_crud(comment):
    if not comment:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Comment not found"
        )


def validate_patch_in_crud(patch):
    if not patch:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Patch not found"
        )


def add_patch_to_history(db, patch, operation, comment):
    db_history_patch = models.History(
        patch=patch, operation=operation, comment=comment
    )
    db.add(db_history_patch)
    db.commit()
    db.refresh(db_history_patch)


def get_patches(db: Session):
    return db.query(models.Patch).all()


def create_patch(db: Session, patch: str, comment: str):
    validate_comment_in_crud(comment)
    db_patch = models.Patch(patch=patch, comment=comment)
    db.add(db_patch)
    add_patch_to_history(db, patch, OpEnum.create, comment=comment)
    db.commit()
    db.refresh(db_patch)
    return db_patch


def del_patches(db: Session, patch_id: int):
    db_patch = db.get(models.Patch, patch_id)
    validate_patch_in_crud(db_patch)
    add_patch_to_history(
        db, db_patch.patch, OpEnum.delete, comment="deleting patch"
    )
    db.delete(db_patch)
    db.commit()
    return {"message": "Patch deleted successfully"}


def put_patches(db: Session, patch_id: int, patch: str, comment: str):
    validate_comment_in_crud(comment)
    db_patch = db.get(models.Patch, patch_id)
    validate_patch_in_crud(db_patch)
    db_patch.patch = patch
    db_patch.timestamp_change = datetime.now()
    db_patch.comment = comment
    add_patch_to_history(db, patch, OpEnum.update, comment)
    db.commit()
    db.refresh(db_patch)
    return db_patch


def get_history_of_changes(db: Session):
    return db.query(models.History).all()
