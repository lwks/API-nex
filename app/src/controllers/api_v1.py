from fastapi import APIRouter
from app.src.controllers.items_controller import router as items_router
from app.src.controllers.users_controller import router as users_router

api_router = APIRouter()
api_router.include_router(items_router, prefix="/items", tags=["items"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
