from typing import Any, Dict, List

from app.src.domain.repositories import RepositoryProtocol
from app.src.models.company import CompanyCreate, CompanyUpdate


class CompaniesService:
    def __init__(self, repo: RepositoryProtocol):
        self.repo = repo

    async def create(self, payload: CompanyCreate) -> str:
        data = payload.model_dump()
        return await self.repo.create(data)

    async def get(self, company_id: str) -> Dict[str, Any] | None:
        return await self.repo.get_by_id(company_id)

    async def update(self, company_id: str, payload: CompanyUpdate) -> bool:
        data = {k: v for k, v in payload.model_dump().items() if v is not None}
        if not data:
            return True
        return await self.repo.update(company_id, data)

    async def delete(self, company_id: str) -> bool:
        return await self.repo.delete(company_id)

    async def list(self, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        return await self.repo.list(skip=skip, limit=limit)
