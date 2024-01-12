import pytest

from src.core.entity.subscription import Subscription
from src.core.interfaces.auth.firebase import IFirebaseApplication
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase
from tests.fixtures.common.mock_functions import (
    mock_firebase_user,
    mock_verify_token_random_user_id,
)
from tests.fixtures.user.db.model import fxm_user_default_3

# pytest tests/main/group/usecases/user/test_user_get.py::test_user -v -s


@pytest.mark.parametrize(
    "firebase_app",
    [{"mock_verify_token": mock_verify_token_random_user_id, "mock_firebase_user": mock_firebase_user}],
    indirect=["firebase_app"],
)
async def test_user_with_token_and_not_in_the_database(
    uow: IUnitOfWork, auth_provider_repository: IAuthProviderRepository, firebase_app: IFirebaseApplication
):
    token = "aboba"
    uc = UserMeUsecase(uow=uow, auth_provider=auth_provider_repository)
    user = await uc(token=token)
    result = user.item
    mock_user = await mock_firebase_user(id="")
    assert result.id == mock_user.id
    assert result.username == mock_user.name
    assert result.active == mock_user.active
    assert result.subscription == Subscription()


@pytest.mark.parametrize(
    "firebase_app",
    [{"mock_verify_token": mock_verify_token_random_user_id, "mock_firebase_user": mock_firebase_user}],
    indirect=["firebase_app"],
)
@pytest.mark.asyncio
async def test_user_with_token_and_in_the_database(
    uow: IUnitOfWork,
    auth_provider_repository: IAuthProviderRepository,
    firebase_app: IFirebaseApplication,
    fxm_user_default_3,
):
    token = "aboba"
    uc = UserMeUsecase(uow=uow, auth_provider=auth_provider_repository)
    user = await uc(token=token)
    result = user.item
    mock_user = await mock_firebase_user(id="")
    assert result.id == mock_user.id
    assert result.username == mock_user.name
    assert result.active == mock_user.active
    assert result.subscription == Subscription()
