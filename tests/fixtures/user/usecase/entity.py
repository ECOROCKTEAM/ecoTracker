import pytest

from src.core.entity.user import User
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE, DEFAULT_TEST_USECASE_USER_ID
from tests.utils import get_random_str


@pytest.fixture(scope="function")
def fxe_user_default() -> User:
    return User(
        id=DEFAULT_TEST_USECASE_USER_ID,
        active=True,
        username=get_random_str(),
        language=DEFAULT_TEST_LANGUAGE,
        subscription="",  # type: ignore
    )


@pytest.fixture(scope="function")
def fxe_user_not_premium() -> User:
    class UserMocked(User):
        @property
        def is_premium(self) -> bool:
            # TODO implement!
            return False

    return UserMocked(
        id=DEFAULT_TEST_USECASE_USER_ID,
        active=True,
        username=get_random_str(),
        language=DEFAULT_TEST_LANGUAGE,
        subscription="",  # type: ignore
    )
