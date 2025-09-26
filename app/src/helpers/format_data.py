from datetime import date, datetime

from app.src.models.company import CompanyOut


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
