from typing import List, Dict, Any
from app.src.domain.repositories import RepositoryProtocol
from app.src.models.item import ItemCreate, ItemUpdate


class ItemsService:
    def __init__(self, repo: RepositoryProtocol):
        self.repo = repo

    async def create(self, payload: ItemCreate) -> str:
        return await self.repo.create(payload.model_dump())

    async def get(self, item_id: str) -> Dict[str, Any] | None:
        return await self.repo.get_by_id(item_id)

    async def update(self, item_id: str, payload: ItemUpdate) -> bool:
        data = {k: v for k, v in payload.model_dump().items() if v is not None}
        if not data:
            return True  # nothing to update but not an error
        return await self.repo.update(item_id, data)

    async def delete(self, item_id: str) -> bool:
        return await self.repo.delete(item_id)

    async def list(self, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        return await self.repo.list(skip=skip, limit=limit)
