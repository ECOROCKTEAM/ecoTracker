from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.mission import MissionGroup
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.group.role import GroupRoleEnum
from src.data.models.challenges.mission import (
    GroupMissionModel,
    MissionModel,
    MissionTranslateModel,
)
from src.data.models.group.group import GroupModel
from src.data.models.user.user import UserGroupModel, UserModel


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_model_no_active_Group(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_mission_model_ru: tuple[MissionModel, MissionTranslateModel],
    test_group_model_not_active: GroupModel,
) -> AsyncGenerator[tuple[GroupModel, MissionModel, GroupMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    user_group = UserGroupModel(
        user_id=test_user_model_ru.id,
        group_id=test_group_model_not_active.id,
        role=GroupRoleEnum.USER,
    )
    group_mission = GroupMissionModel(
        group_id=test_group_model_not_active.id,
        mission_id=mission_model.id,
        author="t",
        status=OccupancyStatusEnum.ACTIVE,
    )
    session.add(user_group)
    session.add(group_mission)
    await session.commit()

    yield (test_group_model_not_active, mission_model, group_mission)

    await session.delete(group_mission)
    await session.delete(user_group)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_model_no_user(
    session: AsyncSession,
    test_mission_model_ru: tuple[MissionModel, MissionTranslateModel],
    test_group_model_public: GroupModel,
) -> AsyncGenerator[tuple[GroupModel, MissionModel, GroupMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    group_mission = GroupMissionModel(
        group_id=test_group_model_public.id,
        mission_id=mission_model.id,
        author="t",
        status=OccupancyStatusEnum.ACTIVE,
    )
    session.add(group_mission)
    await session.commit()

    yield (test_group_model_public, mission_model, group_mission)

    await session.delete(group_mission)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_model_user_blocked(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_mission_model_ru: tuple[MissionModel, MissionTranslateModel],
    test_group_model_public: GroupModel,
) -> AsyncGenerator[tuple[GroupModel, MissionModel, GroupMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    user_group = UserGroupModel(
        user_id=test_user_model_ru.id,
        group_id=test_group_model_public.id,
        role=GroupRoleEnum.BLOCKED,
    )
    group_mission = GroupMissionModel(
        group_id=test_group_model_public.id,
        mission_id=mission_model.id,
        author="t",
        status=OccupancyStatusEnum.ACTIVE,
    )
    session.add(user_group)
    session.add(group_mission)
    await session.commit()

    yield (test_group_model_public, mission_model, group_mission)

    await session.delete(group_mission)
    await session.delete(user_group)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_model_user_admin(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_mission_model_ru: tuple[MissionModel, MissionTranslateModel],
    test_group_model_public: GroupModel,
) -> AsyncGenerator[tuple[GroupModel, MissionModel, GroupMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    user_group = UserGroupModel(
        user_id=test_user_model_ru.id,
        group_id=test_group_model_public.id,
        role=GroupRoleEnum.ADMIN,
    )
    group_mission = GroupMissionModel(
        group_id=test_group_model_public.id,
        mission_id=mission_model.id,
        author="t",
        status=OccupancyStatusEnum.ACTIVE,
    )
    session.add(user_group)
    session.add(group_mission)
    await session.commit()

    yield (test_group_model_public, mission_model, group_mission)

    await session.delete(group_mission)
    await session.delete(user_group)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_user_admin_entity(
    test_group_mission_model_user_admin: tuple[GroupModel, MissionModel, GroupMissionModel]
) -> AsyncGenerator[MissionGroup, None]:
    _, _, group_mission = test_group_mission_model_user_admin
    yield MissionGroup(
        id=group_mission.id,
        group_id=group_mission.group_id,
        mission_id=group_mission.mission_id,
        author=group_mission.author,
        date_start=group_mission.date_start,
        date_close=group_mission.date_close,
        status=group_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_user_admin_finished_entity(
    session: AsyncSession,
    test_group_mission_model_user_admin: tuple[GroupModel, MissionModel, GroupMissionModel],
) -> AsyncGenerator[MissionGroup, None]:
    _, _, group_mission = test_group_mission_model_user_admin
    group_mission.status = OccupancyStatusEnum.FINISH
    session.add(group_mission)
    await session.commit()
    yield MissionGroup(
        id=group_mission.id,
        group_id=group_mission.group_id,
        mission_id=group_mission.mission_id,
        author=group_mission.author,
        date_start=group_mission.date_start,
        date_close=group_mission.date_close,
        status=group_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_no_user_entity(
    test_group_mission_model_no_user: tuple[GroupModel, MissionModel, GroupMissionModel]
) -> AsyncGenerator[MissionGroup, None]:
    _, _, group_mission = test_group_mission_model_no_user
    yield MissionGroup(
        id=group_mission.id,
        group_id=group_mission.group_id,
        mission_id=group_mission.mission_id,
        author=group_mission.author,
        date_start=group_mission.date_start,
        date_close=group_mission.date_close,
        status=group_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_user_blocked_entity(
    test_group_mission_model_user_blocked: tuple[GroupModel, MissionModel, GroupMissionModel]
) -> AsyncGenerator[MissionGroup, None]:
    _, _, group_mission = test_group_mission_model_user_blocked
    yield MissionGroup(
        id=group_mission.id,
        group_id=group_mission.group_id,
        mission_id=group_mission.mission_id,
        author=group_mission.author,
        date_start=group_mission.date_start,
        date_close=group_mission.date_close,
        status=group_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_group_mission_not_active_group_entity(
    test_group_mission_model_no_active_group: tuple[GroupModel, MissionModel, GroupMissionModel]
) -> AsyncGenerator[MissionGroup, None]:
    _, _, group_mission = test_group_mission_model_no_active_group
    yield MissionGroup(
        id=group_mission.id,
        group_id=group_mission.group_id,
        mission_id=group_mission.mission_id,
        author=group_mission.author,
        date_start=group_mission.date_start,
        date_close=group_mission.date_close,
        status=group_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_user_group_user_dto(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_group_model_public: GroupModel,
) -> AsyncGenerator[UserGroupDTO, None]:
    user_group = UserGroupModel(
        user_id=test_user_model_ru.id,
        group_id=test_group_model_public.id,
        role=GroupRoleEnum.USER,
    )
    session.add(user_group)
    await session.commit()

    yield UserGroupDTO(
        user_id=user_group.user_id,
        group_id=user_group.group_id,
        role=user_group.role,
    )

    await session.delete(user_group)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_user_group_admin_dto(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_group_model_public: GroupModel,
) -> AsyncGenerator[UserGroupDTO, None]:
    user_group = UserGroupModel(
        user_id=test_user_model_ru.id,
        group_id=test_group_model_public.id,
        role=GroupRoleEnum.ADMIN,
    )
    session.add(user_group)
    await session.commit()

    yield UserGroupDTO(
        user_id=user_group.user_id,
        group_id=user_group.group_id,
        role=user_group.role,
    )

    await session.delete(user_group)
    await session.commit()
