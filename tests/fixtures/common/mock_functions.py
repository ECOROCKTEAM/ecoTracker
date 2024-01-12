from src.core.dto.auth.firebase import ProviderIdentity, TokenIdentity, UserIdentity
from src.core.enum.auth.providers import AuthProviderEnum


async def mock_firebase_user(id: str) -> UserIdentity:
    return UserIdentity(
        id="aboba_id",
        name="test",
        active=True,
        pic="test",
        email="test",
        email_verified=True,
        provider=ProviderIdentity(type=AuthProviderEnum.GOOGLE, data={}),
    )


async def mock_verify_token_random_user_id(token: str, check_revoked: bool = True) -> TokenIdentity:
    return TokenIdentity(
        user_id="aboba_id",
        name="test",
        email="test",
        email_verified=True,
        pic="test",
        auth_time=1337,
        iss="test",
        aud="test",
        uid="test",
        provider="google.com",
        provider_data={},
        iat=1337,
        exp=1337,
    )
