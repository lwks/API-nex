import pytest
from app.src.models.user import UserCreate
from app.src.services.users_service import UsersService


class InMemoryRepo:
    def __init__(self):
        self.store = {}
        self._seq = 0

    async def create(self, data: dict) -> str:
        self._seq += 1
        _id = str(self._seq)
        self.store[_id] = {"_id": _id, **data}
        return _id

    async def get_by_id(self, id: str):
        return self.store.get(id)


@pytest.mark.anyio("asyncio")
async def test_service_create_and_get():
    repo = InMemoryRepo()
    svc = UsersService(repo)  # type: ignore[arg-type]

    user_id = await svc.create(UserCreate(name="Bob", email="bob@example.com"))
    assert user_id == "1"

    doc = await svc.get(user_id)
    assert doc and doc["name"] == "Bob"
