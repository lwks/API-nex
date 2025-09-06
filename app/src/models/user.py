from app.src.models.base import APIModel


class UserCreate(APIModel):
    name: str
    email: str


class UserOut(APIModel):
    id: str
    name: str
    email: str
