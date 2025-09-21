from __future__ import annotations

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


def _default_tls_ca_file() -> Optional[str]:
    try:
        import certifi  # type: ignore import-not-found
    except ModuleNotFoundError:
        return None

    return certifi.where()


class Settings(BaseSettings):
    APP_NAME: str = "My API"
    API_V1_PREFIX: str = "/api/v1"
    MONGO_URI: str = (
        "mongodb+srv://matheusmatos_db_user:TOz4z3mbXC3LlO2U@cluster.mscrbyb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
    )
    MONGO_DB: str = "mydb"
    MONGO_TLS_CA_FILE: str | None = Field(default_factory=_default_tls_ca_file)
    ENV: str = "dev"

    class Config:
        env_file = ".env"


settings = Settings()
