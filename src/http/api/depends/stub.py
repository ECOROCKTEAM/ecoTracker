from typing import Annotated

from fastapi import Depends

from src.core.entity.user import User
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.http.api.depends.auth import token_header


def get_configure_json_stub() -> dict:
    raise NotImplementedError("Use implement function")


def get_auth_provider_stub() -> IAuthProviderRepository:
    raise NotImplementedError("Use implement function")


def get_uow_stub() -> IUnitOfWork:
    raise NotImplementedError("Use implement function")


def get_user_stub(
    token: Annotated[str, Depends(token_header)],
) -> User:
    raise NotImplementedError("Use implement function")
