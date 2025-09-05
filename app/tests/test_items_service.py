import pytest
from app.src.models.item import ItemCreate, ItemUpdate
from app.src.services.items_service import ItemsService


class InMemoryRepo:
    def __init__(self):
        self.store = {}
        self._seq = 0

    async def get_by_id(self, id: str):
        return self.store.get(id)

    async def create(self, data: dict) -> str:
        self._seq += 1
        _id = str(self._seq)
        self.store[_id] = {"_id": _id, **data}
        return _id

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
async def test_service_create_and_get():
    repo = InMemoryRepo()
    svc = ItemsService(repo)  # type: ignore[arg-type]

    item_id = await svc.create(ItemCreate(name="Book", description="A nice book"))
    assert item_id == "1"

    doc = await svc.get(item_id)
    assert doc and doc["name"] == "Book"

    updated = await svc.update(item_id, ItemUpdate(description="Updated"))
    assert updated

    listed = await svc.list()
    assert len(listed) == 1

    deleted = await svc.delete(item_id)
    assert deleted
