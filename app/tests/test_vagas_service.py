import pytest

from app.src.models.vaga import VagaUpdate
from app.src.services.vagas_service import VagasService


class InMemoryRepo:
    def __init__(self):
        self.store: dict[str, dict] = {}

    async def get_by_id(self, id: str):
        return self.store.get(id)

    async def create(self, data: dict) -> str:
        vaga_id = f"vaga_{len(self.store) + 1:03d}"
        self.store[vaga_id] = {"_id": vaga_id, **data}
        return vaga_id

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
async def test_vagas_service_crud_flow():
    repo = InMemoryRepo()
    svc = VagasService(repo)  # type: ignore[arg-type]

    vaga_id = await svc.create(
        {
            "client_id": "cli_001",
            "titulo": "Analista de Dados",
            "descricao": "Responsavel por analisar dados.",
            "nivel": "Pleno",
            "localizacao": "Sao Paulo/SP",
            "modelo_trabalho": "Hibrido",
            "publicada_em": "2024-03-10",
            "status": "Aberta",
            "skills": ["Python", "SQL"],
            "orcamento": {"valor_inicial": 5500.0, "valor_final": 7500.0},
            "observacoes": "Aceita candidatos em meio periodo.",
        }
    )

    assert vaga_id == "vaga_001"

    fetched = await svc.get(vaga_id)
    assert fetched and fetched["titulo"] == "Analista de Dados"
    assert fetched["modelo_trabalho"] == "Hibrido"
    assert fetched["observacoes"] == "Aceita candidatos em meio periodo."
    assert fetched["orcamento"]["valor_inicial"] == 5500.0

    updated = await svc.update(vaga_id, VagaUpdate(status="Fechada", modelo_trabalho="Remoto"))
    assert updated

    listed = await svc.list()
    assert len(listed) == 1
    assert listed[0]["modelo_trabalho"] == "Remoto"

    deleted = await svc.delete(vaga_id)
    assert deleted
