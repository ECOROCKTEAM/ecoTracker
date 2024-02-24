from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.auth.firebase import FirebaseApplicationSingleton
from src.application.database.manager import db_manager
from src.application.settings import settings
from src.http.configure import setup_fastapi


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.initialize(settings.DATABASE_URL)
    yield
    await db_manager.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Initial firebase
    firebase_app = FirebaseApplicationSingleton(
        name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH
    )
    firebase_app.setup()

    setup_fastapi(app=app, settings=settings)

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
