from typing import Callable, List, Optional

from fastapi import APIRouter, Depends, Query

from app.src.helpers.format_data import FormatData
from app.src.helpers.pagination import Pagination
from app.src.models.candidatura import CandidaturaCreate, CandidaturaOut, CandidaturaUpdate
from app.src.services.candidaturas_service import CandidaturasService

router = APIRouter()

# Provider placeholder wired at runtime in app.src.main
candidaturas_service_provider: Optional[Callable[[], CandidaturasService]] = None


def get_candidaturas_service() -> CandidaturasService:
    if candidaturas_service_provider is None:  # pragma: no cover - wired at runtime
        raise RuntimeError("CandidaturasService provider not wired. Configure at startup.")
    return candidaturas_service_provider()


@router.post("", response_model=str)
async def create_candidatura(
    payload: CandidaturaCreate, svc: CandidaturasService = Depends(get_candidaturas_service)
) -> str:
    return await svc.create(payload)


@router.get("/{company_id}", response_model=CandidaturaOut | None)
async def get_candidatura(
    company_id: str, svc: CandidaturasService = Depends(get_candidaturas_service)
) -> CandidaturaOut | None:
    doc = await svc.get(company_id)
    return None if not doc else FormatData.candidatura_out(doc)


@router.put("/{company_id}", response_model=bool)
async def update_candidatura(
    company_id: str,
    payload: CandidaturaUpdate,
    svc: CandidaturasService = Depends(get_candidaturas_service),
) -> bool:
    return await svc.update(company_id, payload)


@router.delete("/{company_id}", response_model=bool)
async def delete_candidatura(
    company_id: str, svc: CandidaturasService = Depends(get_candidaturas_service)
) -> bool:
    return await svc.delete(company_id)


@router.get("", response_model=List[CandidaturaOut])
async def list_candidaturas(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    svc: CandidaturasService = Depends(get_candidaturas_service),
) -> List[CandidaturaOut]:
    pg = Pagination.clamp(skip, limit)
    docs = await svc.list(skip=pg.skip, limit=pg.limit)
    return [FormatData.candidatura_out(d) for d in docs]
