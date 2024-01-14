from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.auth.firebase import FirebaseApplicationSingleton
from src.application.database.manager import db_manager
from src.application.settings import settings
from src.http.api.depends.deps import (
    get_uow,
    get_uow_stub,
    get_user_dev,
    get_user_prod,
    get_user_stub,
)
from src.http.api.user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.initialize(settings.DATABASE_URL)
    yield
    await db_manager.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Initial firebase
    FirebaseApplicationSingleton(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)

    app.dependency_overrides[get_uow_stub] = get_uow
    # print(F"APP ENV = {settings.APP_ENV.lower()}")
    if settings.APP_ENV.lower() == "prod":
        app.dependency_overrides[get_user_stub] = get_user_prod
    else:
        app.dependency_overrides[get_user_stub] = get_user_dev

    # Routers
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
