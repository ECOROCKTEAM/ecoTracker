import pytest

from src.core.entity.subscription import Subscription
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum
from src.core.exception.base import AuthError
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.user.user_me import UserMeUsecase
from tests.main.auth.test_repository import mock_verify_token_random_user_id


# pytest tests/main/group/usecases/user/test_user_get.py::test_user -v -s
@pytest.mark.parametrize(
    "firebase_app", [{"mock_verify_token": mock_verify_token_random_user_id}], indirect=["firebase_app"]
)
async def test_user_ok(uow: IUnitOfWork, auth_provider_repository: IAuthProviderRepository):
    token = "aboba"
    user_id = "aboba_id"
    with pytest.raises(AuthError) as e:
        uc = UserMeUsecase(uow=uow, auth_provider=auth_provider_repository)
        user = await uc(token=token)
        result = user.item
        assert isinstance(result, User)
        assert isinstance(result.id, str)
        assert isinstance(result.subscription, Subscription)
        assert isinstance(result.username, str)
        assert isinstance(result.active, bool)
        assert isinstance(result.language, LanguageEnum)
    assert f"Error on get user by id={user_id}" in str(e.value)
