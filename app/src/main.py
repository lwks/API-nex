from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient

from app.src.helpers.settings import settings
from app.src.helpers.logging import configure_logging
from app.src.controllers.api_v1 import api_router

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


@app.on_event("shutdown")
async def shutdown() -> None:
    if mongo_client:
        mongo_client.close()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
