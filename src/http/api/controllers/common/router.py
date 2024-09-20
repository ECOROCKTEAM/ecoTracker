from fastapi import APIRouter

from .challenges.mission.mission import router as mission_router
from .challenges.mission.mission_group import router as mission_group_router
from .challenges.mission.mission_user import router as mission_user_router
from .challenges.occupancy.occupancy import router as occupancy_router
from .challenges.task.task import router as task_router
from .challenges.task.task_user import router as task_user_router
from .contact.contact import router as contact_router
from .group.group import router as group_router
from .group.group_user import router as group_user_router
from .score.user_rating import router as user_rating_router
from .score.user_score import router as user_score_router
from .statistic.group import router as statistic_group_router
from .statistic.user import router as statistic_user_router
from .user.user import router as user_router

common_router = APIRouter()
common_router.include_router(occupancy_router, tags=["Occupancy"], prefix="/occupancy")
common_router.include_router(user_router, tags=["User"], prefix="/user")
common_router.include_router(contact_router, tags=["Contact"], prefix="/user/contact")
common_router.include_router(user_score_router, tags=["User score"], prefix="/user/score")
common_router.include_router(user_rating_router, tags=["User rating"], prefix="/user/rating")
common_router.include_router(task_router, tags=["Task"], prefix="/task")
common_router.include_router(task_user_router, tags=["User task"], prefix="/user/task")

common_router.include_router(statistic_group_router, tags=["Group statistic"], prefix="/statistic/group")
common_router.include_router(statistic_user_router, tags=["User statistic"], prefix="/statistic/user")

common_router.include_router(mission_router, tags=["Mission"], prefix="/mission")
common_router.include_router(mission_user_router, tags=["Mission user"], prefix="/user/mission")
common_router.include_router(mission_group_router, tags=["Mission group"], prefix="")

common_router.include_router(group_router, tags=["Group"], prefix="/group")
common_router.include_router(group_user_router, tags=["Group User"], prefix="")
