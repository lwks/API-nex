import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.src.controllers.vagas_controller import get_vagas_service, router
from app.src.models.vaga import VagaCreate, VagaUpdate


class InMemoryVagasService:
    """Simple in-memory service used to demonstrate the vagas endpoints."""

    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Any]] = {}
        self._counter = 0

    async def create(self, payload: VagaCreate) -> str:
        self._counter += 1
        vaga_id = f"vaga_{self._counter:03d}"
        self._data[vaga_id] = {"_id": vaga_id, **payload.model_dump()}
        return vaga_id

    async def get(self, vaga_id: str) -> Dict[str, Any] | None:
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

    async def list(self, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        vagas = list(self._data.values())
        return vagas[skip : skip + limit]


def format_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)


def build_app() -> FastAPI:
    app = FastAPI()
    service = InMemoryVagasService()
    app.dependency_overrides[get_vagas_service] = lambda: service
    app.include_router(router, prefix="/api/v1/vagas")
    return app


async def run_demo() -> None:
    app = build_app()
    transport = ASGITransport(app=app)

    payload = {
        "client_id": "cli_001",
        "titulo": "Analista de Dados",
        "descricao": "Responsável por relatórios e dashboards.",
        "nivel": "Senior",
        "localizacao": "Remoto",
        "publicada_em": "2024-03-10",
        "status": "Aberta",
        "skills": ["Python", "AWS", "Testes"],
    }

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        post_response = await client.post("/api/v1/vagas", json=payload)
        get_all_response = await client.get("/api/v1/vagas")

    print("POST /api/v1/vagas payload:")
    print(format_json(payload))
    print()
    print("POST response status:", post_response.status_code)
    print("POST response body:")
    print(format_json(post_response.json()))
    print()
    print("GET /api/v1/vagas response status:", get_all_response.status_code)
    print("GET /api/v1/vagas response body:")
    print(format_json(get_all_response.json()))


if __name__ == "__main__":
    asyncio.run(run_demo())
