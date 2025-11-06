from typing import Any, Callable, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, Query

from app.src.helpers.format_data import FormatData
from app.src.helpers.pagination import Pagination
from app.src.models.vaga import VagaOut, VagaUpdate
from app.src.services.vagas_service import VagasService

router = APIRouter()

# Provider placeholder wired at runtime in app.src.main
vagas_service_provider: Optional[Callable[[], VagasService]] = None


def get_vagas_service() -> VagasService:
    if vagas_service_provider is None:  # pragma: no cover - wired at runtime
        raise RuntimeError("VagasService provider not wired. Configure at startup.")
    return vagas_service_provider()


@router.post("", response_model=str)
async def create_vaga(
    payload: Dict[str, Any] = Body(...),
    svc: VagasService = Depends(get_vagas_service),
) -> str:
    return await svc.create(payload)


@router.get("/{vaga_id}", response_model=VagaOut | None)
async def get_vaga(vaga_id: str, svc: VagasService = Depends(get_vagas_service)) -> VagaOut | None:
    doc = await svc.get(vaga_id)
    return None if not doc else FormatData.vaga_out(doc)


@router.put("/{vaga_id}", response_model=bool)
async def update_vaga(
    vaga_id: str, payload: VagaUpdate, svc: VagasService = Depends(get_vagas_service)
) -> bool:
    return await svc.update(vaga_id, payload)


@router.delete("/{vaga_id}", response_model=bool)
async def delete_vaga(vaga_id: str, svc: VagasService = Depends(get_vagas_service)) -> bool:
    return await svc.delete(vaga_id)


@router.get("", response_model=List[VagaOut])
async def list_vagas(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    svc: VagasService = Depends(get_vagas_service),
) -> List[VagaOut]:
    pg = Pagination.clamp(skip, limit)
    docs = await svc.list(skip=pg.skip, limit=pg.limit)
    return [FormatData.vaga_out(d) for d in docs]
