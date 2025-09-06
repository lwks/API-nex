from typing import List, Callable, Optional
from fastapi import APIRouter, Depends, Query
from app.src.models.item import ItemCreate, ItemUpdate, ItemOut
from app.src.helpers.pagination import Pagination
from app.src.services.items_service import ItemsService

router = APIRouter()

# Provider placeholder wired at runtime in app.src.main
items_service_provider: Optional[Callable[[], ItemsService]] = None


def get_items_service() -> ItemsService:
    if items_service_provider is None:  # pragma: no cover - wired at runtime
        raise RuntimeError("ItemsService provider not wired. Configure at startup.")
    return items_service_provider()

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
