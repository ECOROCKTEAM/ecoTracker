import pytest

from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase
from tests.fixtures.user.db.model import fxm_user_default, fxm_user_not_active


# pytest tests/main/group/usecases/user/test_user_get.py::test_user -v -s
@pytest.mark.asyncio
async def test_user_ok(uow: IUnitOfWork, fxm_user_default: User):
    uc = UserMeUsecase(uow=uow)
    user = await uc(user_id=fxm_user_default.id)
    result = user.item
    assert isinstance(result, User)
    assert result.id == fxm_user_default.id
    assert result.username == fxm_user_default.username
    assert result.password == fxm_user_default.password
    assert result.active == fxm_user_default.active
    assert result.language == fxm_user_default.language


@pytest.mark.asyncio
async def test_user_fail(uow: IUnitOfWork, fxm_user_not_active: User):
    uc = UserMeUsecase(uow=uow)
    with pytest.raises(UserIsNotActivateError):
        await uc(user_id=fxm_user_not_active.id)
