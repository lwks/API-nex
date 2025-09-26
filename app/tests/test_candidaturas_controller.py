import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.src.controllers.candidaturas_controller import (
    get_candidaturas_service,
    router,
)
from app.src.models.candidatura import CandidaturaCreate, CandidaturaUpdate


class FakeService:
    def __init__(self):
        self._data: dict[str, dict] = {}

    async def create(self, payload: CandidaturaCreate) -> str:
        self._data[payload.company_id] = {
            "_id": payload.company_id,
            **payload.model_dump(exclude={"company_id"}),
            "company_id": payload.company_id,
        }
        return payload.company_id

    async def get(self, company_id: str):
        return self._data.get(company_id)

    async def update(self, company_id: str, payload: CandidaturaUpdate) -> bool:
        if company_id not in self._data:
            return False
        for field, value in payload.model_dump().items():
            if value is not None:
                self._data[company_id][field] = value
        return True

    async def delete(self, company_id: str) -> bool:
        return self._data.pop(company_id, None) is not None

    async def list(self, skip: int = 0, limit: int = 20):
        candidaturas = list(self._data.values())
        return candidaturas[skip : skip + limit]


@pytest.mark.anyio("asyncio")
async def test_candidaturas_controller_crud_flow():
    app = FastAPI()
    svc = FakeService()
    app.dependency_overrides[get_candidaturas_service] = lambda: svc
    app.include_router(router, prefix="/api/v1/candidaturas")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "company_id": "comp_001",
            "name": "Tech Corp",
            "email": "contact@techcorp.com",
            "password_hash": "hashedpwd",
            "phone": "+55 11 99999-9999",
            "website": "https://techcorp.com",
            "location": {
                "city": "São Paulo",
                "state": "SP",
                "country": "Brasil",
            },
            "about": "Empresa de tecnologia focada em IA.",
            "industry": "Tecnologia",
            "size": "51-100",
            "founded_year": 2015,
            "social_links": {
                "linkedin": "https://linkedin.com/company/techcorp",
                "instagram": "https://instagram.com/techcorp",
            },
            "logo_url": "https://cdn.techcorp.com/logo.png",
            "created_at": "2024-01-10T10:00:00",
            "updated_at": "2024-01-10T10:00:00",
        }

        resp = await ac.post("/api/v1/candidaturas", json=payload)
        assert resp.status_code == 200
        assert resp.json() == "comp_001"

        resp = await ac.get("/api/v1/candidaturas/comp_001")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Tech Corp"

        resp = await ac.get("/api/v1/candidaturas")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        resp = await ac.put(
            "/api/v1/candidaturas/comp_001",
            json={"size": "101-200"},
        )
        assert resp.status_code == 200
        assert resp.json() is True

        resp = await ac.delete("/api/v1/candidaturas/comp_001")
        assert resp.status_code == 200
        assert resp.json() is True
