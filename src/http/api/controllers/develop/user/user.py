from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase
from src.http.api.depends.stub import (
    get_auth_provider_stub,
    get_configure_json_stub,
    get_uow_stub,
)
from src.http.api.schemas.user import UserSchema

router = APIRouter()


@router.get(
    "/user/list",
)
async def dev_user_list(
    configure_json: Annotated[dict, Depends(get_configure_json_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    auth_provider: Annotated[IAuthProviderRepository, Depends(get_auth_provider_stub)],
) -> list[UserSchema]:
    user_id_list = [user["id"] for user in configure_json["develop_user_list"]]
    uc = UserMeUsecase(uow=uow, auth_provider=auth_provider)
    user_list = []
    for user_id in user_id_list:
        result = await uc(token=user_id)
        user_list.append(result.item)
    user_schema_list = [UserSchema.from_obj(user) for user in user_list]
    return user_schema_list
