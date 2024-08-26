from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): pass


class Patch(Base):
    __tablename__ = "patches"

    id = Column(Integer, primary_key=True)
    patch = Column(String)
