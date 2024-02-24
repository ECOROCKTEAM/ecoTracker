import json

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.database.base import build_engine, create_session_factory
from src.application.settings import settings
from src.core.dto.auth.firebase import AuthProviderEnum, ProviderIdentity, UserIdentity
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.data.repository.auth import AuthProviderRepository


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    engine = build_engine(settings.DATABASE_URL)
    sf = create_session_factory(engine=engine)
    return sf


def read_develop_json() -> dict:
    with open(settings.CONFIGURE_JSON_PATH) as f:
        data = json.load(f)
    return data


def get_mock_auth_provider(user_identity_list: list) -> IAuthProviderRepository:
    class AuthProviderRepositoryMocked(AuthProviderRepository):
        def __init__(self) -> None:
            pass

        async def get_user_by_token(self, token: str, check_revoked: bool = True) -> UserIdentity:
            data = {
                user_identity["id"]: UserIdentity(
                    id=user_identity["id"],
                    name=user_identity["name"],
                    active=user_identity["active"],
                    pic=user_identity["pic"],
                    email=user_identity["email"],
                    email_verified=user_identity["email_verified"],
                    provider=ProviderIdentity(
                        type=AuthProviderEnum[user_identity["provider"]["type"]], data=user_identity["provider"]["data"]
                    ),
                )
                for user_identity in user_identity_list
            }
            return data[token]

    return AuthProviderRepositoryMocked()
