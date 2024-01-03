import os

import pytest

from src.core.dto.auth.firebase import ProviderIdentity, TokenIdentity, UserIdentity
from src.core.exception.base import AuthError
from src.core.interfaces.repository.auth import IAuthProviderRepository

# Tests commented bcs need deps from env

# # pytest tests/main/auth/test_repository.py::test_get_user_by_token -v -s
# async def test_get_user_by_token(auth_provider_repository: IAuthProviderRepository):
#     token = os.environ.get("FB_USER_TOKEN")
#     if token is None:
#         raise NotImplementedError("FB token not set for test")
#     user_identity = await auth_provider_repository.get_user_by_token(token=token)
#     assert isinstance(user_identity, UserIdentity)
#     assert isinstance(user_identity.provider, ProviderIdentity)


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


# pytest tests/main/auth/test_repository.py::test_token_error -v -s
async def test_token_error(auth_provider_repository: IAuthProviderRepository):
    token = "aboba"
    with pytest.raises(AuthError) as e:
        await auth_provider_repository.get_user_by_token(token=token)
    assert "Error on verify token" in str(e.value)


# pytest tests/main/auth/test_repository.py::test_user_get_error -v -s
@pytest.mark.parametrize(
    "firebase_app", [{"mock_verify_token": mock_verify_token_random_user_id}], indirect=["firebase_app"]
)
async def test_user_get_error(auth_provider_repository: IAuthProviderRepository):
    user_id = "aboba_id"
    token = "aboba"
    with pytest.raises(AuthError) as e:
        await auth_provider_repository.get_user_by_token(token=token)
    assert f"Error on get user by id={user_id}" in str(e.value)
