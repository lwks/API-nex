from typing import List, Dict, Any

from app.src.domain.repositories import RepositoryProtocol
from app.src.helpers.custom_exception import InvalidIdentifierError
from app.src.models.item import ItemCreate, ItemUpdate


class ItemsService:
    def __init__(self, repo: RepositoryProtocol):
        self.repo = repo

    async def create(self, payload: ItemCreate) -> str:
        return await self.repo.create(payload.model_dump())

    async def get(self, item_id: str) -> Dict[str, Any] | None:
        try:
            return await self.repo.get_by_id(item_id)
        except InvalidIdentifierError:
            return None

    async def update(self, item_id: str, payload: ItemUpdate) -> bool:
        data = {k: v for k, v in payload.model_dump().items() if v is not None}
        if not data:
            return True  # nothing to update but not an error
        try:
            return await self.repo.update(item_id, data)
        except InvalidIdentifierError:
            return False

    async def delete(self, item_id: str) -> bool:
        try:
            return await self.repo.delete(item_id)
        except InvalidIdentifierError:
            return False

    async def list(self, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        return await self.repo.list(skip=skip, limit=limit)
