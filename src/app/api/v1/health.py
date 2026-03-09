from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    status: str


@router.get("", response_model=HealthResponse)
async def health_check():
    """Health check"""
    return {"status": "ok"}
