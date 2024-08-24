from sqlalchemy import Column, Integer, String

from .database import Base


class Patch(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    patch = Column(String)
