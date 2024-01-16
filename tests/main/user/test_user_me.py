import pytest
from sqlalchemy import delete

from src.core.entity.subscription import Subscription
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase
from src.data.models.user.user import UserModel
from tests.fixtures.common.mock_functions import (
    mock_get_user,
    mock_verify_token_random_user_id,
)
from tests.fixtures.user.db.model import fxm_user_default_3


# pytest tests/main/group/usecases/user/test_user_me.py::test_user_auto_register_ok -v -s
@pytest.mark.parametrize(
    "firebase_app",
    [{"mock_verify_token": mock_verify_token_random_user_id, "mock_get_user": mock_get_user}],
    indirect=["firebase_app"],
)
async def test_user_auto_register_ok(uow: IUnitOfWork, auth_provider_repository: IAuthProviderRepository, session):
    token = "aboba"
    uc = UserMeUsecase(uow=uow, auth_provider=auth_provider_repository)
    user = await uc(token=token)
    result = user.item
    assert result.id == "aboba_id"
    assert result.username == "test"
    assert result.active is True
    assert result.subscription == Subscription()
    stmt = delete(UserModel).where(UserModel.id == result.id).returning(UserModel.id)
    await session.scalar(stmt)
    await session.commit()


# pytest tests/main/group/usecases/user/test_user_me.py::test_user_already_exist -v -s
@pytest.mark.parametrize(
    "firebase_app",
    [{"mock_verify_token": mock_verify_token_random_user_id, "mock_get_user": mock_get_user}],
    indirect=["firebase_app"],
)
@pytest.mark.asyncio
async def test_user_already_exist(
    uow: IUnitOfWork,
    auth_provider_repository: IAuthProviderRepository,
    fxm_user_default_3,
):
    token = "aboba"
    uc = UserMeUsecase(uow=uow, auth_provider=auth_provider_repository)
    user = await uc(token=token)
    result = user.item
    assert result.id == "aboba_id"
    assert result.username == "test"
    assert result.active is True
    assert result.subscription == Subscription()
