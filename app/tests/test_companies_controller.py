import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.src.controllers.companies_controller import (
    get_companies_service,
    router,
)
from app.src.models.company import CompanyCreate, CompanyUpdate


class FakeService:
    def __init__(self):
        self._data: dict[str, dict] = {}

    async def create(self, payload: CompanyCreate) -> str:
        self._data[payload.id] = {"_id": payload.id, **payload.model_dump(exclude={"id"})}
        return payload.id

    async def get(self, company_id: str):
        return self._data.get(company_id)

    async def update(self, company_id: str, payload: CompanyUpdate) -> bool:
        if company_id not in self._data:
            return False
        for field, value in payload.model_dump().items():
            if value is not None:
                self._data[company_id][field] = value
        return True

    async def delete(self, company_id: str) -> bool:
        return self._data.pop(company_id, None) is not None

    async def list(self, skip: int = 0, limit: int = 20):
        companies = list(self._data.values())
        return companies[skip : skip + limit]


@pytest.mark.anyio("asyncio")
async def test_companies_controller_crud_flow():
    app = FastAPI()
    svc = FakeService()
    app.dependency_overrides[get_companies_service] = lambda: svc
    app.include_router(router, prefix="/api/v1/companies")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "id": "cli_001",
            "nome": "Tech Corp",
            "cnpj": "11.111.111/0001-11",
            "setor": "Tecnologia",
            "localizacao": "Rio de Janeiro/RJ",
            "criado_em": "2024-02-01",
            "vagas": ["Backend", "Frontend"],
        }

        resp = await ac.post("/api/v1/companies", json=payload)
        assert resp.status_code == 200
        assert resp.json() == "cli_001"

        resp = await ac.get("/api/v1/companies/cli_001")
        assert resp.status_code == 200
        assert resp.json()["nome"] == "Tech Corp"

        resp = await ac.get("/api/v1/companies")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        resp = await ac.put(
            "/api/v1/companies/cli_001",
            json={"setor": "Finanças", "vagas": ["Analista"]},
        )
        assert resp.status_code == 200
        assert resp.json() is True

        resp = await ac.delete("/api/v1/companies/cli_001")
        assert resp.status_code == 200
        assert resp.json() is True
