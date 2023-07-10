from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.settings import settings

# from .api.challenges.mission.apis.mission import router as mission_router
# from .api.challenges.mission.apis.mission_user import router as mission_user_router
# from .api.challenges.mission.apis.mission_community import router as mission_community_router
# from .api.challenges.task.apis.task import router as task_router
from .api.challenges.task.apis.task_user import router as task_user_router
from .api.community.apis.community_api import router as community_router
from .api.deps import db_manager
from .api.occupancy.apis.api import router as occupancy_router
from .api.score.apis.score_community_api import router as score_community_router
from .api.score.apis.score_user_api import router as score_user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.initialize(settings.DATABASE_URL)
    yield
    await db_manager.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.include_router(community_router)
    # app.include_router(mission_router)
    # app.include_router(mission_user_router)
    # app.include_router(mission_community_router)
    # app.include_router(task_router)
    app.include_router(task_user_router)
    app.include_router(score_user_router)
    app.include_router(score_community_router)
    app.include_router(occupancy_router)
    return app
