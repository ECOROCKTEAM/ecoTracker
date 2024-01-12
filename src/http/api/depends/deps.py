from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from src.application.database.manager import db_manager
from src.core.entity.user import User
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase, UserMeUsecaseDevelop
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
    auth_provider: Annotated[IAuthProviderRepository, Depends(get_auth_provider_stub)],
) -> User:
    print(f"dev {token=}")
    # something do with token and get user id
    uc = UserMeUsecaseDevelop(uow=uow, auth_provider=auth_provider)
    result = await uc(token=token)
    return result.item
