from boto3.session import Session
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.src.aws_services.dynamodb_service import DynamoDBService
from app.src.controllers.api_v1 import api_router
import app.src.controllers.candidaturas_controller as candidaturas_controller
import app.src.controllers.companies_controller as companies_controller
import app.src.controllers.items_controller as items_controller
import app.src.controllers.users_controller as users_controller
import app.src.controllers.vagas_controller as vagas_controller
from app.src.helpers.logging import configure_logging
from app.src.helpers.settings import settings
from app.src.services.candidaturas_service import CandidaturasService
from app.src.services.companies_service import CompaniesService
from app.src.services.items_service import ItemsService
from app.src.services.repositories.dynamo_candidaturas_repository import (
    DynamoCandidaturasRepository,
)
from app.src.services.repositories.dynamo_companies_repository import DynamoCompaniesRepository
from app.src.services.repositories.dynamo_items_repository import DynamoItemsRepository
from app.src.services.repositories.dynamo_users_repository import DynamoUsersRepository
from app.src.services.repositories.dynamo_vagas_repository import DynamoVagasRepository
from app.src.services.users_service import UsersService
from app.src.services.vagas_service import VagasService

app = FastAPI(title=settings.APP_NAME, docs_url="/docs")
configure_logging()

dynamo_session: Session | None = None


@app.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup() -> None:
    global dynamo_session
    dynamo_session = Session(region_name=settings.AWS_REGION)
    endpoint_url = settings.DYNAMODB_ENDPOINT_URL

    items_repo = DynamoItemsRepository(
        DynamoDBService(
            settings.DYNAMODB_ITEMS_TABLE,
            session=dynamo_session,
            endpoint_url=endpoint_url,
        )
    )
    items_svc = ItemsService(items_repo)

    users_repo = DynamoUsersRepository(
        DynamoDBService(
            settings.DYNAMODB_USERS_TABLE,
            session=dynamo_session,
            endpoint_url=endpoint_url,
        )
    )
    users_svc = UsersService(users_repo)

    companies_repo = DynamoCompaniesRepository(
        DynamoDBService(
            settings.DYNAMODB_COMPANIES_TABLE,
            session=dynamo_session,
            endpoint_url=endpoint_url,
        )
    )
    companies_svc = CompaniesService(companies_repo)

    candidaturas_repo = DynamoCandidaturasRepository(
        DynamoDBService(
            settings.DYNAMODB_CANDIDATURAS_TABLE,
            session=dynamo_session,
            endpoint_url=endpoint_url,
        )
    )
    candidaturas_svc = CandidaturasService(candidaturas_repo)

    vagas_repo = DynamoVagasRepository(
        DynamoDBService(
            settings.DYNAMODB_VAGAS_TABLE,
            session=dynamo_session,
            endpoint_url=endpoint_url,
        )
    )
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


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
