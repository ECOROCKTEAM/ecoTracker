from datetime import datetime
from random import randint

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.data.models.group.group import GroupModel
from src.data.models.user.user import UserGroupModel, UserModel
from src.data.repository.group import user_group_model_to_dto
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE
from tests.utils import get_random_str


# pytest tests/main/group/test_group_list.py::test_group_user_list_ok -v -s
@pytest.mark.asyncio
async def test_group_user_list_ok(session: AsyncSession):
    user_list = []
    user_with_request = UserModel(
        id="The Witcher", username="Geralt of Rivia", active=True, language=DEFAULT_TEST_LANGUAGE
    )

    user_list.append(user_with_request)
    for _ in range(5):
        random_user = UserModel(
            id=get_random_str(), username=get_random_str(), active=True, language=DEFAULT_TEST_LANGUAGE
        )
        user_list.append(random_user)

    group = GroupModel(
        id=randint(1, 1984),
        name="Test Group",
        description="",
        active=True,
        privacy=GroupPrivacyEnum.PUBLIC,
        code=get_random_str(),
        code_expire_time=datetime.now(),
    )

    session.add_all([group, *user_list])
    await session.commit()

    user_group_list = []

    for user in user_list:
        user_group = UserGroupModel(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)
        user_group_list.append(user_group)

    session.add_all([*user_group_list])
    await session.commit()

    for user_group in user_group_list:
        await session.delete(user_group)
        await session.commit()

    for user in user_list:
        await session.delete(user)
        await session.commit()
    await session.delete(group)
