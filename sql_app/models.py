import enum

from sqlalchemy import Column, DateTime, Enum, Integer, JSON, String
from sqlalchemy.orm import DeclarativeBase, validates
from sqlalchemy.sql import func


class OpEnum(enum.Enum):
    create = 1
    update = 2
    delete = 3


class Base(DeclarativeBase):
    pass


class BasePatch(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, nullable=False)
    patch = Column(JSON, nullable=False)
    timestamp_change = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    comment = Column(String, nullable=False)
    service = Column(String, nullable=False)
    stage = Column(String, nullable=False)
    user = Column(String, nullable=False)


class Patch(BasePatch):
    __tablename__ = "patches"

    @validates("comment")
    def validate_comment(self, key, comment):
        if comment == "":
            raise ValueError("An empty comment is not allowed")
        return comment


class History(BasePatch):
    __tablename__ = "history"

    operation = Column(Enum(OpEnum), nullable=False)
