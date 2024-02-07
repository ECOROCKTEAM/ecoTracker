from fastapi import APIRouter

from .user.user import router as user_router

develop_router = APIRouter(prefix="/develop", tags=["Develop"])
develop_router.include_router(user_router)
