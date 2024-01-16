from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from src.application.auth.firebase import FirebaseApplicationSingleton
from src.application.database.manager import db_manager
from src.application.settings import settings
from src.core.entity.user import User
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase, UserMeUsecaseDevelop
from src.data.repository.auth import AuthProviderRepository
from src.data.unit_of_work import SqlAlchemyUnitOfWork

token_header = APIKeyHeader(name="Authorization", scheme_name="Authorization", auto_error=True)

# Stubs


def get_auth_provider_stub() -> IAuthProviderRepository:
    raise NotImplementedError("Use implement function")


def get_uow_stub() -> IUnitOfWork:
    raise NotImplementedError("Use implement function")


def get_user_stub(
    token: Annotated[str, Depends(token_header)],
) -> User:
    raise NotImplementedError("Use implement function")


# Implemented depends


def get_uow() -> IUnitOfWork:
    return SqlAlchemyUnitOfWork(db_manager.session_factory)


def get_auth_provider_prod() -> IAuthProviderRepository:
    firebase_app = FirebaseApplicationSingleton(
        name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH
    )
    return AuthProviderRepository(firebase_app=firebase_app)


async def get_user_prod(
    token: Annotated[str, Depends(token_header)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    auth_provider: Annotated[IAuthProviderRepository, Depends(get_auth_provider_stub)],
) -> User:
    print(f"prod {token=}")
    # something do with token and get user id
    # user_id = "aboba..."
    uc = UserMeUsecase(uow=uow, auth_provider=auth_provider)
    result = await uc(token=token)
    return result.item


async def get_user_dev(
    token: Annotated[str | None, Depends(token_header)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> User:
    print(f"dev {token=}")
    # something do with token and get user id
    uc = UserMeUsecaseDevelop(uow=uow)
    result = await uc(token=token)
    return result.item
