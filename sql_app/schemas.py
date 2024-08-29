from pydantic import BaseModel


class Patch(BaseModel):
    patch: dict
    comment: str

    class Config:
        from_attributes = True
