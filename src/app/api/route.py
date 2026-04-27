from fastapi import APIRouter

from app.api.v1 import health, users


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(users.router)
