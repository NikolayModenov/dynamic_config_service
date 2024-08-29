import enum

from sqlalchemy import Column, DateTime, Enum, Integer, JSON, String
from sqlalchemy.orm import DeclarativeBase, validates
from sqlalchemy.sql import func


class OpEnum(enum.Enum):
    create = 1
    update = 2
    delete = 3


class Base(DeclarativeBase): pass


class Patch(Base):
    __tablename__ = "patches"

    id = Column(Integer, primary_key=True, nullable=False)
    patch = Column(JSON, nullable=False)
    timestamp_change = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now(),
        nullable=False
    )
    comment = Column(String, nullable=False)

    @validates("comment")
    def validate_comment(self, key, comment):
        if comment == "":
            raise ValueError("An empty comment is not allowed")
        return comment


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    patch = Column(JSON, nullable=False)
    operation = Column(Enum(OpEnum), nullable=False)
    timestamp_change = Column(
        DateTime, server_default=func.now(), nullable=False
    )
    comment = Column(String, nullable=False)
