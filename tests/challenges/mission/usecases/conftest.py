from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.user import User
from src.data.models.user.user import UserModel


@pytest_asyncio.fixture(scope="function")
async def test_user_premium_ru_entity(test_user_model_ru: UserModel) -> AsyncGenerator[User, None]:
    yield User(
        id=test_user_model_ru.id,
        active=test_user_model_ru.active,
        username=test_user_model_ru.username,
        password=test_user_model_ru.password,
        language=test_user_model_ru.language,
        subscription="",  # type: ignore
    )


@pytest_asyncio.fixture(scope="function")
async def test_user_premium_en_entity(test_user_model_en: UserModel) -> AsyncGenerator[User, None]:
    yield User(
        id=test_user_model_en.id,
        active=test_user_model_en.active,
        username=test_user_model_en.username,
        password=test_user_model_en.password,
        language=test_user_model_en.language,
        subscription="",  # type: ignore
    )


@pytest_asyncio.fixture(scope="function")
async def test_user_not_premium_entity(test_user_model_ru: UserModel) -> AsyncGenerator[User, None]:
    class UserMocked(User):
        @property
        def is_premium(self) -> bool:
            # TODO implement!
            return False

    yield UserMocked(
        id=test_user_model_ru.id,
        active=test_user_model_ru.active,
        username=test_user_model_ru.username,
        password=test_user_model_ru.password,
        language=test_user_model_ru.language,
        subscription="",  # type: ignore
    )
