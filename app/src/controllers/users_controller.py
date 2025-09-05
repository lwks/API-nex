from fastapi import APIRouter, Depends
from app.src.models.user import UserCreate, UserOut
from app.src.services.users_service import UsersService


router = APIRouter()


def get_users_service() -> UsersService:  # pragma: no cover - replaced at runtime
    raise NotImplementedError


def _to_user_out(doc: dict) -> UserOut:
    return UserOut(id=str(doc.get("_id") or doc.get("id")), name=doc["name"], email=doc["email"])


@router.post("", response_model=str)
async def create_user(payload: UserCreate, svc: UsersService = Depends(get_users_service)) -> str:
    return await svc.create(payload)


@router.get("/{user_id}", response_model=UserOut | None)
async def get_user(user_id: str, svc: UsersService = Depends(get_users_service)) -> UserOut | None:
    doc = await svc.get(user_id)
    return None if not doc else _to_user_out(doc)
