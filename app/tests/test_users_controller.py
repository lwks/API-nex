import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from app.src.controllers.users_controller import router, get_users_service
from app.src.models.user import UserCreate


class FakeService:
    def __init__(self):
        self._seq = 0
        self._data = {}

    async def create(self, payload: UserCreate) -> str:
        self._seq += 1
        _id = str(self._seq)
        self._data[_id] = {"_id": _id, **payload.model_dump()}
        return _id

    async def get(self, user_id: str):
        return self._data.get(user_id)


@pytest.mark.anyio("asyncio")
async def test_create_and_get_user():
    app = FastAPI()
    svc = FakeService()
    app.dependency_overrides[get_users_service] = lambda: svc
    app.include_router(router, prefix="/api/v1/users")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/users",
            json={"name": "Alice", "email": "alice@example.com"},
        )
        assert resp.status_code == 200
        user_id = resp.json()
        assert user_id == "1"

        resp = await ac.get(f"/api/v1/users/{user_id}")
        assert resp.status_code == 200
        assert resp.json()["email"] == "alice@example.com"
