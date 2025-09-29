import pytest

from app.src.models.candidatura import CandidaturaCreate, CandidaturaUpdate
from app.src.services.candidaturas_service import CandidaturasService


class InMemoryRepo:
    def __init__(self):
        self.store = {}

    async def get_by_id(self, id: str):
        return self.store.get(id)

    async def create(self, data: dict) -> str:
        company_id = data["company_id"]
        self.store[company_id] = {"_id": company_id, **data}
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
async def test_candidaturas_service_crud_flow():
    repo = InMemoryRepo()
    svc = CandidaturasService(repo)  # type: ignore[arg-type]

    payload = CandidaturaCreate(
        company_id="comp_001",
        name="Tech Corp",
        email="contact@techcorp.com",
        password_hash="hashedpwd",
        phone="+55 11 99999-9999",
        website="https://techcorp.com",
        location={
            "city": "São Paulo",
            "state": "SP",
            "country": "Brasil",
        },
        about="Empresa de tecnologia focada em IA.",
        industry="Tecnologia",
        size="51-100",
        founded_year=2015,
        social_links={
            "linkedin": "https://linkedin.com/company/techcorp",
            "instagram": "https://instagram.com/techcorp",
        },
        logo_url="https://cdn.techcorp.com/logo.png",
        created_at="2024-01-10T10:00:00",
        updated_at="2024-01-10T10:00:00",
    )

    created_id = await svc.create(payload)
    assert created_id == "comp_001"

    fetched = await svc.get(created_id)
    assert fetched and fetched["name"] == "Tech Corp"

    updated = await svc.update(created_id, CandidaturaUpdate(size="101-200"))
    assert updated

    listed = await svc.list()
    assert len(listed) == 1

    deleted = await svc.delete(created_id)
    assert deleted
