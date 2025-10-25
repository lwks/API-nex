from typing import Any, Dict, List

from app.src.domain.repositories import RepositoryProtocol
from app.src.helpers.custom_exception import InvalidIdentifierError
from app.src.models.vaga import VagaUpdate


class VagasService:
    def __init__(self, repo: RepositoryProtocol):
        self.repo = repo

    async def create(self, payload: Dict[str, Any]) -> str:
        data = dict(payload)
        return await self.repo.create(data)

    async def get(self, vaga_id: str) -> Dict[str, Any] | None:
        try:
            return await self.repo.get_by_id(vaga_id)
        except InvalidIdentifierError:
            return None

    async def update(self, vaga_id: str, payload: VagaUpdate) -> bool:
        data = {k: v for k, v in payload.model_dump().items() if v is not None}
        if not data:
            return True
        try:
            return await self.repo.update(vaga_id, data)
        except InvalidIdentifierError:
            return False

    async def delete(self, vaga_id: str) -> bool:
        try:
            return await self.repo.delete(vaga_id)
        except InvalidIdentifierError:
            return False

    async def list(self, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        return await self.repo.list(skip=skip, limit=limit)
