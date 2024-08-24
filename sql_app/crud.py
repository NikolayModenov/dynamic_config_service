from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy.orm import Session

from . import models


def get_patches(db: Session):
    return db.query(models.Patch).all()


def create_patch(db: Session, patch: str):
    db_patch = models.Patch(patch=patch)
    db.add(db_patch)
    db.commit()
    db.refresh(db_patch)
    return db_patch


def del_patches(db: Session, patch_id: int):
    db_patch = db.get(models.Patch, patch_id)
    if not db_patch:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Patch not found"
        )
    db.delete(db_patch)
    db.commit()
    return {"message": "Patch deleted successfully"}


def put_patches(db: Session, patch_id: int, patch: str):
    db_patch = db.get(models.Patch, patch_id)
    db_patch.patch = patch
    db.commit()
    return db_patch
