import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.src.controllers.vagas_controller import get_vagas_service, router
from app.src.models.vaga import VagaCreate, VagaUpdate


class FakeService:
    def __init__(self):
        self._data: dict[str, dict] = {}
        self._counter = 0

    async def create(self, payload: VagaCreate) -> str:
        self._counter += 1
        vaga_id = f"vaga_{self._counter:03d}"
        self._data[vaga_id] = {"_id": vaga_id, **payload.model_dump()}
        return vaga_id

    async def get(self, vaga_id: str):
        return self._data.get(vaga_id)

    async def update(self, vaga_id: str, payload: VagaUpdate) -> bool:
        if vaga_id not in self._data:
            return False
        for field, value in payload.model_dump().items():
            if value is not None:
                self._data[vaga_id][field] = value
        return True

    async def delete(self, vaga_id: str) -> bool:
        return self._data.pop(vaga_id, None) is not None

    async def list(self, skip: int = 0, limit: int = 20):
        vagas = list(self._data.values())
        return vagas[skip : skip + limit]


@pytest.mark.anyio("asyncio")
async def test_vagas_controller_crud_flow():
    app = FastAPI()
    svc = FakeService()
    app.dependency_overrides[get_vagas_service] = lambda: svc
    app.include_router(router, prefix="/api/v1/vagas")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "client_id": "cli_001",
            "titulo": "Analista de Dados",
            "descricao": "Responsável por relatórios.",
            "nivel": "Senior",
            "localizacao": "Remoto",
            "publicada_em": "2024-03-10",
            "status": "Aberta",
            "skills": ["Python", "AWS"],
            "orcamento": {"valor_inicial": 5000.0, "valor_final": 8000.0},
        }

        resp = await ac.post("/api/v1/vagas", json=payload)
        assert resp.status_code == 200
        vaga_id = resp.json()
        assert vaga_id == "vaga_001"

        resp = await ac.get(f"/api/v1/vagas/{vaga_id}")
        assert resp.status_code == 200
        assert resp.json()["titulo"] == "Analista de Dados"

        resp = await ac.get("/api/v1/vagas")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        resp = await ac.put(
            f"/api/v1/vagas/{vaga_id}",
            json={"status": "Fechada", "skills": ["Python", "SQL"]},
        )
        assert resp.status_code == 200
        assert resp.json() is True

        resp = await ac.delete(f"/api/v1/vagas/{vaga_id}")
        assert resp.status_code == 200
        assert resp.json() is True
