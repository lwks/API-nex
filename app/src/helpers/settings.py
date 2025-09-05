from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "My API"
    API_V1_PREFIX: str = "/api/v1"
    MONGO_URI: str = (
        "mongodb+srv://matheusmatos_db_user:TOz4z3mbXC3LlO2U@cluster.mscrbyb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
    )
    MONGO_DB: str = "mydb"
    ENV: str = "dev"

    class Config:
        env_file = ".env"


settings = Settings()
