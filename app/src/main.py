from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from app.src.helpers.settings import settings
from app.src.helpers.logging import configure_logging
from app.src.controllers.api_v1 import api_router
from app.src.services.repositories.mongo_candidaturas_repository import (
    MongoCandidaturasRepository,
)
from app.src.services.repositories.mongo_companies_repository import MongoCompaniesRepository
from app.src.services.repositories.mongo_items_repository import MongoItemsRepository
from app.src.services.repositories.mongo_users_repository import MongoUsersRepository
from app.src.services.repositories.mongo_vagas_repository import MongoVagasRepository
from app.src.services.items_service import ItemsService
from app.src.services.users_service import UsersService
from app.src.services.candidaturas_service import CandidaturasService
from app.src.services.companies_service import CompaniesService
from app.src.services.vagas_service import VagasService
import app.src.controllers.items_controller as items_controller
import app.src.controllers.users_controller as users_controller
import app.src.controllers.companies_controller as companies_controller
import app.src.controllers.candidaturas_controller as candidaturas_controller
import app.src.controllers.vagas_controller as vagas_controller

app = FastAPI(title=settings.APP_NAME, docs_url="/docs")
configure_logging()

mongo_client: AsyncIOMotorClient | None = None


@app.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup() -> None:
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    items_repo = MongoItemsRepository(mongo_client, settings.MONGO_DB)
    items_svc = ItemsService(items_repo)
    users_repo = MongoUsersRepository(mongo_client, settings.MONGO_DB)
    users_svc = UsersService(users_repo)
    companies_repo = MongoCompaniesRepository(mongo_client, settings.MONGO_DB)
    companies_svc = CompaniesService(companies_repo)
    candidaturas_repo = MongoCandidaturasRepository(mongo_client, settings.MONGO_DB)
    candidaturas_svc = CandidaturasService(candidaturas_repo)
    vagas_repo = MongoVagasRepository(mongo_client, settings.MONGO_DB)
    vagas_svc = VagasService(vagas_repo)

    def _items_provider() -> ItemsService:
        return items_svc

    def _users_provider() -> UsersService:
        return users_svc

    def _companies_provider() -> CompaniesService:
        return companies_svc


    def _candidaturas_provider() -> CandidaturasService:
        return candidaturas_svc

    def _vagas_provider() -> VagasService:
        return vagas_svc


    # simple dependency injection via provider variables
    items_controller.items_service_provider = _items_provider  # type: ignore[attr-defined]
    users_controller.users_service_provider = _users_provider  # type: ignore[attr-defined]
    companies_controller.companies_service_provider = _companies_provider  # type: ignore[attr-defined]
    candidaturas_controller.candidaturas_service_provider = _candidaturas_provider  # type: ignore[attr-defined]
    vagas_controller.vagas_service_provider = _vagas_provider  # type: ignore[attr-defined]


@app.on_event("shutdown")
async def shutdown() -> None:
    if mongo_client:
        mongo_client.close()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
