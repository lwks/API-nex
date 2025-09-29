from datetime import date, datetime

from app.src.models.candidatura import CandidaturaOut
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
    def _parse_datetime(value: datetime | str | None) -> datetime | None:
        if value is None or isinstance(value, datetime):
            return value
        iso_value = value
        if iso_value.endswith("Z"):
            iso_value = iso_value[:-1] + "+00:00"
        return datetime.fromisoformat(iso_value)

    @staticmethod
    def candidatura_out(doc: dict) -> CandidaturaOut:
        """Normalize a persistence document into ``CandidaturaOut`` payload."""
        company_id = str(doc.get("_id") or doc.get("company_id"))

        created_at_value = FormatData._parse_datetime(doc.get("created_at"))
        updated_at_value = FormatData._parse_datetime(doc.get("updated_at"))

        location = doc.get("location") or {}
        social_links = doc.get("social_links") or {}

        return CandidaturaOut(
            company_id=company_id,
            name=doc["name"],
            email=doc["email"],
            password_hash=doc["password_hash"],
            phone=doc["phone"],
            website=doc["website"],
            location=location,
            about=doc["about"],
            industry=doc["industry"],
            size=doc["size"],
            founded_year=doc["founded_year"],
            social_links=social_links,
            logo_url=doc["logo_url"],
            created_at=created_at_value,
            updated_at=updated_at_value,

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
