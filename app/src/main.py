from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.helpers.settings import settings
from app.helpers.logging import configure_logging
from app.controllers.api_v1 import api_router
from app.services.repositories.mongo_items_repository import MongoItemsRepository
from app.services.items_service import ItemsService
import app.controllers.items_controller as items_controller

app = FastAPI(title=settings.APP_NAME)
configure_logging()

mongo_client: AsyncIOMotorClient | None = None

@app.on_event("startup")
async def startup() -> None:
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    repo = MongoItemsRepository(mongo_client, settings.MONGO_DB)
    svc = ItemsService(repo)

    def _provider() -> ItemsService:
        return svc

    # simple dependency injection
    items_controller.get_items_service = _provider  # type: ignore[attr-defined]

@app.on_event("shutdown")
async def shutdown() -> None:
    if mongo_client:
        mongo_client.close()

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
