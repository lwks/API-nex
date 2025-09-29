from datetime import date, datetime

from app.src.models.company import CompanyOut
from app.src.models.vaga import VagaOut


class FormatData:
    """Utility helpers to map raw persistence documents into API models."""

    @staticmethod
    def company_out(doc: dict) -> CompanyOut:
        """Normalize a persistence document into ``CompanyOut`` payload."""
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

    @staticmethod
    def vaga_out(doc: dict) -> VagaOut:
        """Normalize a persistence document into ``VagaOut`` payload."""
        vaga_id = str(doc.get("_id") or doc.get("id"))
        publicada_em_value = doc.get("publicada_em")

        if isinstance(publicada_em_value, str):
            publicada_em_value = date.fromisoformat(publicada_em_value)
        elif isinstance(publicada_em_value, datetime):
            publicada_em_value = publicada_em_value.date()

        return VagaOut(
            id=vaga_id,
            client_id=doc["client_id"],
            titulo=doc["titulo"],
            descricao=doc["descricao"],
            nivel=doc["nivel"],
            localizacao=doc["localizacao"],
            publicada_em=publicada_em_value,
            status=doc["status"],
            skills=doc.get("skills", []),
        )
