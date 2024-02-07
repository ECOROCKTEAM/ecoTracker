import json
from typing import Annotated

from fastapi import Depends

from src.application.database.manager import db_manager
from src.application.settings import settings
from src.core.entity.user import User
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase
from src.data.unit_of_work import SqlAlchemyUnitOfWork
from src.http.api.depends.auth import token_header
from src.http.api.depends.stub import get_auth_provider_stub, get_uow_stub


def get_configure_json() -> dict:
    with open(settings.CONFIGURE_JSON_PATH) as f:
        data = json.load(f)
    return data


def get_uow() -> IUnitOfWork:
    return SqlAlchemyUnitOfWork(db_manager.session_factory)


async def get_user(
    token: Annotated[str, Depends(token_header)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    auth_provider: Annotated[IAuthProviderRepository, Depends(get_auth_provider_stub)],
) -> User:
    uc = UserMeUsecase(uow=uow, auth_provider=auth_provider)
    result = await uc(token=token)
    return result.item
