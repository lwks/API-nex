from typing import Dict, Any

from app.src.domain.repositories import RepositoryProtocol
from app.src.helpers.custom_exception import InvalidIdentifierError
from app.src.models.user import UserCreate


class UsersService:
    def __init__(self, repo: RepositoryProtocol):
        self.repo = repo

    async def create(self, payload: UserCreate) -> str:
        return await self.repo.create(payload.model_dump())

    async def get(self, user_id: str) -> Dict[str, Any] | None:
        try:
            return await self.repo.get_by_id(user_id)
        except InvalidIdentifierError:
            return None
