from fastapi import APIRouter

from .contact.contact import router as contact_router
from .user.user import router as user_router

common_router = APIRouter()
common_router.include_router(user_router, tags=["User"], prefix="/user")
common_router.include_router(contact_router, tags=["Contact"], prefix="/user/contact")
