from datetime import datetime

from app.src.models.base import APIModel


class ApplicationLocation(APIModel):
    city: str
    state: str
    country: str


class ApplicationSocialLinks(APIModel):
    linkedin: str | None = None
    instagram: str | None = None


class CandidaturaBase(APIModel):
    company_id: str
    name: str
    email: str
    password_hash: str
    phone: str
    website: str
    location: ApplicationLocation
    about: str
    industry: str
    size: str
    founded_year: int
    social_links: ApplicationSocialLinks
    logo_url: str
    created_at: datetime
    updated_at: datetime


class CandidaturaCreate(CandidaturaBase):
    pass


class CandidaturaUpdate(APIModel):
    name: str | None = None
    email: str | None = None
    password_hash: str | None = None
    phone: str | None = None
    website: str | None = None
    location: ApplicationLocation | None = None
    about: str | None = None
    industry: str | None = None
    size: str | None = None
    founded_year: int | None = None
    social_links: ApplicationSocialLinks | None = None
    logo_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CandidaturaOut(CandidaturaBase):
    pass
