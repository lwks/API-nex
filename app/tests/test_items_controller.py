import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from app.controllers.items_controller import router, get_items_service
from app.models.item import ItemCreate, ItemUpdate

class FakeService:
    def __init__(self):
        self._seq = 0
        self._data = {}

    async def create(self, payload: ItemCreate) -> str:
        self._seq += 1
        _id = str(self._seq)
        self._data[_id] = {"_id": _id, **payload.model_dump()}
        return _id

    async def get(self, item_id: str):
        return self._data.get(item_id)

    async def update(self, item_id: str, payload: ItemUpdate) -> bool:
        if item_id not in self._data:
            return False
        for k, v in payload.model_dump().items():
            if v is not None:
                self._data[item_id][k] = v
        return True

    async def delete(self, item_id: str) -> bool:
        return self._data.pop(item_id, None) is not None

    async def list(self, skip: int = 0, limit: int = 20):
        items = list(self._data.values())
        return items[skip: skip + limit]

@pytest.mark.anyio
async def test_controller_crud():
    app = FastAPI()
    # dependency override for tests
    app.dependency_overrides[get_items_service] = lambda: FakeService()
    app.include_router(router, prefix="/api/v1/items")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create
        resp = await ac.post("/api/v1/items", json={"name": "Pen", "description": "Blue"})
        assert resp.status_code == 200
        item_id = resp.json()
        assert item_id == "1"

        # get
        resp = await ac.get(f"/api/v1/items/{item_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Pen"

        # list
        resp = await ac.get("/api/v1/items")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        # update
        resp = await ac.patch(f"/api/v1/items/{item_id}", json={"description": "Black"})
        assert resp.status_code == 200
        assert resp.json() is True

        # delete
        resp = await ac.delete(f"/api/v1/items/{item_id}")
        assert resp.status_code == 200
        assert resp.json() is True
