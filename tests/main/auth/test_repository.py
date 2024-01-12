import os

import pytest

from src.core.dto.auth.firebase import ProviderIdentity, TokenIdentity, UserIdentity
from src.core.exception.base import AuthError
from src.core.interfaces.repository.auth import IAuthProviderRepository
from tests.fixtures.common.mock_functions import mock_verify_token_random_user_id

# Tests commented bcs need deps from env

# pytest tests/main/auth/test_repository.py::test_get_user_by_token -v -s
# async def test_get_user_by_token(auth_provider_repository: IAuthProviderRepository):
#     token = os.environ.get("FB_USER_TOKEN")
#     if token is None:
#         raise NotImplementedError("FB token not set for test")
#     user_identity = await auth_provider_repository.get_user_by_token(token=token)
#     assert isinstance(user_identity, UserIdentity)
#     assert isinstance(user_identity.provider, ProviderIdentity)


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
