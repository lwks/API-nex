from datetime import date, datetime
from typing import Callable, List, Optional

from fastapi import APIRouter, Depends, Query

from app.src.helpers.pagination import Pagination
from app.src.models.company import CompanyCreate, CompanyOut, CompanyUpdate
from app.src.services.companies_service import CompaniesService

router = APIRouter()

# Provider placeholder wired at runtime in app.src.main
companies_service_provider: Optional[Callable[[], CompaniesService]] = None


def get_companies_service() -> CompaniesService:
    if companies_service_provider is None:  # pragma: no cover - wired at runtime
        raise RuntimeError("CompaniesService provider not wired. Configure at startup.")
    return companies_service_provider()


def _to_company_out(doc: dict) -> CompanyOut:
    company_id = str(doc.get("_id") or doc.get("id"))
    criado_em_value = doc.get("criado_em")
    if isinstance(criado_em_value, str):
        criado_em_value = date.fromisoformat(criado_em_value)
    elif isinstance(criado_em_value, datetime):
        criado_em_value = criado_em_value.date()
    return CompanyOut(
        id=company_id,
        nome=doc["nome"],
        cnpj=doc["cnpj"],
        setor=doc["setor"],
        localizacao=doc["localizacao"],
        criado_em=criado_em_value,
        vagas=doc["vagas"],
    )


@router.post("", response_model=str)
async def create_company(
    payload: CompanyCreate, svc: CompaniesService = Depends(get_companies_service)
) -> str:
    return await svc.create(payload)


@router.get("/{company_id}", response_model=CompanyOut | None)
async def get_company(
    company_id: str, svc: CompaniesService = Depends(get_companies_service)
) -> CompanyOut | None:
    doc = await svc.get(company_id)
    return None if not doc else _to_company_out(doc)


@router.put("/{company_id}", response_model=bool)
async def update_company(
    company_id: str,
    payload: CompanyUpdate,
    svc: CompaniesService = Depends(get_companies_service),
) -> bool:
    return await svc.update(company_id, payload)


@router.delete("/{company_id}", response_model=bool)
async def delete_company(
    company_id: str, svc: CompaniesService = Depends(get_companies_service)
) -> bool:
    return await svc.delete(company_id)


@router.get("", response_model=List[CompanyOut])
async def list_companies(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    svc: CompaniesService = Depends(get_companies_service),
) -> List[CompanyOut]:
    pg = Pagination.clamp(skip, limit)
    docs = await svc.list(skip=pg.skip, limit=pg.limit)
    return [_to_company_out(d) for d in docs]
