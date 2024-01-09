import pytest

from src.core.entity.subscription import Subscription
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase
from tests.fixtures.user.db.model import fxm_user_not_active


# pytest tests/main/group/usecases/user/test_user_get.py::test_user -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("firebase_app", [], indirect=["firebase_app"])
async def test_user_ok(uow: IUnitOfWork, auth_provider_repository):
    uc = UserMeUsecase(uow=uow, auth_provider=auth_provider_repository)
    """ You can get token in flutter app. """
    token = ""
    user = await uc(token=token)
    result = user.item
    assert isinstance(result, User)
    assert isinstance(result.id, str)
    assert isinstance(result.subscription, Subscription)
    assert isinstance(result.username, str)
    assert isinstance(result.active, bool)
    assert isinstance(result.language, LanguageEnum)


# @pytest.mark.asyncio
# async def test_user_fail(uow: IUnitOfWork, auth_provider_repository, fxm_user_not_active: User):
#     uc = UserMeUsecase(uow=uow, auth_provider=auth_provider_repository)
#     with pytest.raises(UserIsNotActivateError):
#         await uc(token="123")
