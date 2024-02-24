from fastapi import APIRouter

from .user.user import router as user_router

common_router = APIRouter()
common_router.include_router(user_router, tags=["User"], prefix="/user")
