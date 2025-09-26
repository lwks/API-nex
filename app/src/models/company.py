from datetime import date
from typing import List

from app.src.models.base import APIModel


class CompanyBase(APIModel):
    nome: str
    cnpj: str
    setor: str
    localizacao: str
    criado_em: date
    vagas: List[str]


class CompanyCreate(CompanyBase):
    id: str


class CompanyUpdate(APIModel):
    nome: str | None = None
    cnpj: str | None = None
    setor: str | None = None
    localizacao: str | None = None
    criado_em: date | None = None
    vagas: List[str] | None = None


class CompanyOut(CompanyBase):
    id: str
