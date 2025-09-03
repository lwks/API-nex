from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "My API"
    API_V1_PREFIX: str = "/api/v1"
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "mydb"
    ENV: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()
