from app.src.models.base import APIModel

class ItemCreate(APIModel):
    name: str
    description: str | None = None

class ItemUpdate(APIModel):
    name: str | None = None
    description: str | None = None

class ItemOut(APIModel):
    id: str
    name: str
    description: str | None = None
