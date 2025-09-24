import pytest

from app.src.models.company import CompanyCreate, CompanyUpdate
from app.src.services.companies_service import CompaniesService


class InMemoryRepo:
    def __init__(self):
        self.store = {}

    async def get_by_id(self, id: str):
        return self.store.get(id)

    async def create(self, data: dict) -> str:
        company_id = data["id"]
        self.store[company_id] = {"_id": company_id, **{k: v for k, v in data.items() if k != "id"}}
        return company_id

    async def update(self, id: str, data: dict) -> bool:
        if id not in self.store:
            return False
        self.store[id].update(data)
        return True

    async def delete(self, id: str) -> bool:
        return self.store.pop(id, None) is not None

    async def list(self, *, skip: int = 0, limit: int = 20):
        items = list(self.store.values())
        return items[skip : skip + limit]


@pytest.mark.anyio("asyncio")
async def test_companies_service_crud_flow():
    repo = InMemoryRepo()
    svc = CompaniesService(repo)  # type: ignore[arg-type]

    company_id = await svc.create(
        CompanyCreate(
            id="cli_001",
            nome="Acme",
            cnpj="00.000.000/0000-00",
            setor="Tecnologia",
            localizacao="São Paulo/SP",
            criado_em="2024-01-01",
            vagas=["Dev", "QA"],
        )
    )
    assert company_id == "cli_001"

    fetched = await svc.get(company_id)
    assert fetched and fetched["nome"] == "Acme"

    updated = await svc.update(company_id, CompanyUpdate(setor="Fintech"))
    assert updated

    listed = await svc.list()
    assert len(listed) == 1

    deleted = await svc.delete(company_id)
    assert deleted
