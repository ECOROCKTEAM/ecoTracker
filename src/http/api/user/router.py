from fastapi import APIRouter

from src.http.api.user.apis.user import router as auth_router

router = APIRouter(tags=["User"], prefix="/user")
router.include_router(auth_router)
