from fastapi import APIRouter

from .contact.contact import router as contact_router
from .score.user_rating import router as user_rating_router
from .score.user_score import router as user_score_router
from .statistic.group import router as statistic_group_router
from .statistic.user import router as statistic_user_router
from .user.user import router as user_router

common_router = APIRouter()
common_router.include_router(user_router, tags=["User"], prefix="/user")
common_router.include_router(contact_router, tags=["Contact"], prefix="/user/contact")
common_router.include_router(user_score_router, tags=["User score"], prefix="/user/score")
common_router.include_router(user_rating_router, tags=["User rating"], prefix="/user/rating")

common_router.include_router(statistic_group_router, tags=["Group statistic"], prefix="/statistic/group")
common_router.include_router(statistic_user_router, tags=["User statistic"], prefix="/statistic/user")
