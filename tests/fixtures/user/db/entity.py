from collections.abc import AsyncGenerator

import pytest_asyncio

from src.core.entity.user import User
from src.data.models.user.user import UserModel
from tests.fixtures.user.db.model import fxm_user_default


def user_model_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        active=model.active,
        language=model.language,
        subscription="",  # type: ignore
    )


@pytest_asyncio.fixture(scope="function")
async def fxe_user_default(fxm_user_default: UserModel) -> AsyncGenerator[User, None]:
    yield user_model_to_entity(fxm_user_default)
