from fastapi import FastAPI

from src.application.settings import Settings
from src.http.api.controllers.common.router import common_router
from src.http.api.controllers.develop.router import develop_router
from src.http.api.depends import common, develop, prod, stub  # , test


def setup_fastapi_prod(app: FastAPI, settings: Settings):
    app.debug = False
    app.dependency_overrides[stub.get_auth_provider_stub] = prod.get_auth_provider


def setup_fastapi_test(app: FastAPI, settings: Settings):
    app.debug = True
    # app.dependency_overrides[stub.get_user_stub] = test.get_user
    return


def setup_fastapi_dev(app: FastAPI, settings: Settings):
    app.debug = True
    app.dependency_overrides[stub.get_auth_provider_stub] = develop.get_auth_provider
    app.include_router(develop_router)


def setup_fastapi(app: FastAPI, settings: Settings):
    env = settings.APP_ENV.lower()
    # Deps
    app.dependency_overrides[stub.get_user_stub] = common.get_user
    app.dependency_overrides[stub.get_uow_stub] = common.get_uow
    app.dependency_overrides[stub.get_configure_json_stub] = common.get_configure_json
    # Routers
    app.include_router(common_router)

    func_map = dict(dev=setup_fastapi_dev, test=setup_fastapi_test, prod=setup_fastapi_prod)
    func_by_env = func_map[env]
    func_by_env(app=app, settings=settings)
