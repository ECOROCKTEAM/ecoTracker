from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.settings import settings

# from .api.challenges.mission.apis.mission import router as mission_router
# from .api.challenges.mission.apis.mission_user import router as mission_user_router
# from .api.challenges.mission.apis.mission_group import router as mission_group_router
# from .api.challenges.task.apis.task import router as task_router
# from .api.challenges.task.apis.task_user import router as task_user_router
# from .api.group.apis.group_api import router as group_router
# from .api.occupancy.apis.api import router as occupancy_router
# from .api.score.apis.score_group_api import router as score_group_router
# from .api.score.apis.score_user_api import router as score_user_router
from src.http.api.user.router import router as user_router

from .api.depends import db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.initialize(settings.DATABASE_URL)
    yield
    await db_manager.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(user_router)
    # app.include_router(group_router)
    # app.include_router(mission_router)
    # app.include_router(mission_user_router)
    # app.include_router(mission_group_router)
    # app.include_router(task_router)
    # app.include_router(task_user_router)
    # app.include_router(score_user_router)
    # app.include_router(score_group_router)
    # app.include_router(occupancy_router)
    return app
