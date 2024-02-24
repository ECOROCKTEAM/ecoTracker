from typing import Annotated

from fastapi import Depends

from src.core.dto.auth.firebase import ProviderIdentity, UserIdentity
from src.core.enum.auth.providers import AuthProviderEnum
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.data.repository.auth import AuthProviderRepository
from src.http.api.depends.stub import get_configure_json_stub


def get_auth_provider(configure_json: Annotated[dict, Depends(get_configure_json_stub)]) -> IAuthProviderRepository:
    def convert_to_user_identity(item) -> UserIdentity:
        return UserIdentity(
            id=item["id"],
            name=item["name"],
            active=item["active"],
            pic=item["pic"],
            email=item["email"],
            email_verified=item["email_verified"],
            provider=ProviderIdentity(type=AuthProviderEnum[item["provider"]["type"]], data=item["provider"]["data"]),
        )

    user_identity_list = configure_json["develop_user_list"]
    user_identity_dict: dict[str, UserIdentity] = {
        user_identity["id"]: convert_to_user_identity(user_identity) for user_identity in user_identity_list
    }

    class AuthProviderRepositoryMocked(AuthProviderRepository):
        def __init__(self) -> None:
            pass

        async def get_user_by_token(self, token: str, check_revoked: bool = True) -> UserIdentity:
            return user_identity_dict[token]

    return AuthProviderRepositoryMocked()
