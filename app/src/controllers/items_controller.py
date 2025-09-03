from typing import List
from fastapi import APIRouter, Depends, Query
from app.models.item import ItemCreate, ItemUpdate, ItemOut
from app.helpers.pagination import Pagination
from app.services.items_service import ItemsService

router = APIRouter()

# This provider is replaced/wired in app.main at startup.
def get_items_service() -> ItemsService:  # pragma: no cover - replaced at runtime
    raise NotImplementedError

def _to_item_out(doc: dict) -> ItemOut:
    return ItemOut(id=str(doc.get("_id") or doc.get("id")), name=doc["name"], description=doc.get("description"))

@router.post("", response_model=str)
async def create_item(payload: ItemCreate, svc: ItemsService = Depends(get_items_service)) -> str:
    return await svc.create(payload)

@router.get("/{item_id}", response_model=ItemOut | None)
async def get_item(item_id: str, svc: ItemsService = Depends(get_items_service)) -> ItemOut | None:
    doc = await svc.get(item_id)
    return None if not doc else _to_item_out(doc)

@router.patch("/{item_id}", response_model=bool)
async def update_item(item_id: str, payload: ItemUpdate, svc: ItemsService = Depends(get_items_service)) -> bool:
    return await svc.update(item_id, payload)

@router.delete("/{item_id}", response_model=bool)
async def delete_item(item_id: str, svc: ItemsService = Depends(get_items_service)) -> bool:
    return await svc.delete(item_id)

@router.get("", response_model=List[ItemOut])
async def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    svc: ItemsService = Depends(get_items_service),
) -> List[ItemOut]:
    pg = Pagination.clamp(skip, limit)
    docs = await svc.list(skip=pg.skip, limit=pg.limit)
    return [_to_item_out(d) for d in docs]
