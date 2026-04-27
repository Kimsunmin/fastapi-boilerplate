from fastapi import APIRouter

from app.common.responses import ok

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check():
    """Health check"""
    return ok(message="ok")
