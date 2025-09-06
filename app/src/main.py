from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.src.helpers.settings import settings
from app.src.helpers.logging import configure_logging
from app.src.controllers.api_v1 import api_router
from app.src.services.repositories.mongo_items_repository import MongoItemsRepository
from app.src.services.items_service import ItemsService
from app.src.services.repositories.mongo_users_repository import MongoUsersRepository
from app.src.services.users_service import UsersService
import app.src.controllers.items_controller as items_controller
import app.src.controllers.users_controller as users_controller

app = FastAPI(title=settings.APP_NAME)
configure_logging()

mongo_client: AsyncIOMotorClient | None = None


@app.on_event("startup")
async def startup() -> None:
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    items_repo = MongoItemsRepository(mongo_client, settings.MONGO_DB)
    items_svc = ItemsService(items_repo)
    users_repo = MongoUsersRepository(mongo_client, settings.MONGO_DB)
    users_svc = UsersService(users_repo)

    def _items_provider() -> ItemsService:
        return items_svc

    def _users_provider() -> UsersService:
        return users_svc

    # simple dependency injection via provider variables
    items_controller.items_service_provider = _items_provider  # type: ignore[attr-defined]
    users_controller.users_service_provider = _users_provider  # type: ignore[attr-defined]


@app.on_event("shutdown")
async def shutdown() -> None:
    if mongo_client:
        mongo_client.close()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
