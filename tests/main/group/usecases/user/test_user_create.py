import pytest

from src.core.entity.subscription import Subscription
from src.core.entity.user import User, UserCreateDTO
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_create import UserCreateUseCase
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE
from tests.utils import get_random_str


@pytest.mark.asyncio
async def test_user_create(uow: IUnitOfWork):
    uc = UserCreateUseCase(uow=uow)
    obj = UserCreateDTO(id=get_random_str(), username=get_random_str(), active=True, language=DEFAULT_TEST_LANGUAGE)
    user_create = await uc(obj=obj)
    result = user_create.item
    assert isinstance(result, User)
    assert result.id == obj.id
    assert result.username == obj.username
    assert result.active == obj.active
    assert result.subscription == Subscription()
    assert result.language == obj.language
