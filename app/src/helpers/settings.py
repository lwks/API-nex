from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "My API"
    API_V1_PREFIX: str = "/api/v1"
    AWS_REGION: str = "us-east-1"
    DYNAMODB_ENDPOINT_URL: str | None = None
    DYNAMODB_ITEMS_TABLE: str = "items"
    DYNAMODB_USERS_TABLE: str = "users"
    DYNAMODB_COMPANIES_TABLE: str = "companies"
    DYNAMODB_CANDIDATURAS_TABLE: str = "candidaturas"
    DYNAMODB_VAGAS_TABLE: str = "vagas"
    ENV: str = "dev"

    class Config:
        env_file = ".env"


settings = Settings()
