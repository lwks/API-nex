from datetime import date
from typing import List

from app.src.models.base import APIModel


class VagaOrcamento(APIModel):
    valor_inicial: float
    valor_final: float


class VagaBase(APIModel):
    client_id: str
    titulo: str
    descricao: str
    nivel: str
    localizacao: str
    publicada_em: date
    status: str
    skills: List[str]
    orcamento: VagaOrcamento


class VagaCreate(VagaBase):
    pass


class VagaUpdate(APIModel):
    client_id: str | None = None
    titulo: str | None = None
    descricao: str | None = None
    nivel: str | None = None
    localizacao: str | None = None
    publicada_em: date | None = None
    status: str | None = None
    skills: List[str] | None = None
    orcamento: VagaOrcamento | None = None


class VagaOut(VagaBase):
    id: str
