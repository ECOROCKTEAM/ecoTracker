from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.mission import MissionCommunity
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.community.role import CommunityRoleEnum
from src.data.models.challenges.mission import (
    CommunityMissionModel,
    MissionModel,
    MissionTranslateModel,
)
from src.data.models.community.community import CommunityModel
from src.data.models.user.user import UserCommunityModel, UserModel


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_model_no_active_community(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_mission_model_ru: tuple[MissionModel, MissionTranslateModel],
    test_community_model_not_active: CommunityModel,
) -> AsyncGenerator[tuple[CommunityModel, MissionModel, CommunityMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    user_community = UserCommunityModel(
        user_id=test_user_model_ru.id,
        community_id=test_community_model_not_active.id,
        role=CommunityRoleEnum.USER,
    )
    community_mission = CommunityMissionModel(
        community_id=test_community_model_not_active.id,
        mission_id=mission_model.id,
        author="t",
        status=OccupancyStatusEnum.ACTIVE,
    )
    session.add(user_community)
    session.add(community_mission)
    await session.commit()

    yield (test_community_model_not_active, mission_model, community_mission)

    await session.delete(community_mission)
    await session.delete(user_community)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_model_no_user(
    session: AsyncSession,
    test_mission_model_ru: tuple[MissionModel, MissionTranslateModel],
    test_community_model_public: CommunityModel,
) -> AsyncGenerator[tuple[CommunityModel, MissionModel, CommunityMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    community_mission = CommunityMissionModel(
        community_id=test_community_model_public.id,
        mission_id=mission_model.id,
        author="t",
        status=OccupancyStatusEnum.ACTIVE,
    )
    session.add(community_mission)
    await session.commit()

    yield (test_community_model_public, mission_model, community_mission)

    await session.delete(community_mission)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_model_user_blocked(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_mission_model_ru: tuple[MissionModel, MissionTranslateModel],
    test_community_model_public: CommunityModel,
) -> AsyncGenerator[tuple[CommunityModel, MissionModel, CommunityMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    user_community = UserCommunityModel(
        user_id=test_user_model_ru.id,
        community_id=test_community_model_public.id,
        role=CommunityRoleEnum.BLOCKED,
    )
    community_mission = CommunityMissionModel(
        community_id=test_community_model_public.id,
        mission_id=mission_model.id,
        author="t",
        status=OccupancyStatusEnum.ACTIVE,
    )
    session.add(user_community)
    session.add(community_mission)
    await session.commit()

    yield (test_community_model_public, mission_model, community_mission)

    await session.delete(community_mission)
    await session.delete(user_community)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_model_user_admin(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_mission_model_ru: tuple[MissionModel, MissionTranslateModel],
    test_community_model_public: CommunityModel,
) -> AsyncGenerator[tuple[CommunityModel, MissionModel, CommunityMissionModel], None]:
    mission_model, _ = test_mission_model_ru
    user_community = UserCommunityModel(
        user_id=test_user_model_ru.id,
        community_id=test_community_model_public.id,
        role=CommunityRoleEnum.ADMIN,
    )
    community_mission = CommunityMissionModel(
        community_id=test_community_model_public.id,
        mission_id=mission_model.id,
        author="t",
        status=OccupancyStatusEnum.ACTIVE,
    )
    session.add(user_community)
    session.add(community_mission)
    await session.commit()

    yield (test_community_model_public, mission_model, community_mission)

    await session.delete(community_mission)
    await session.delete(user_community)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_user_admin_entity(
    test_community_mission_model_user_admin: tuple[CommunityModel, MissionModel, CommunityMissionModel]
) -> AsyncGenerator[MissionCommunity, None]:
    _, _, community_mission = test_community_mission_model_user_admin
    yield MissionCommunity(
        id=community_mission.id,
        community_id=community_mission.community_id,
        mission_id=community_mission.mission_id,
        author=community_mission.author,
        date_start=community_mission.date_start,
        date_close=community_mission.date_close,
        status=community_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_user_admin_finished_entity(
    session: AsyncSession,
    test_community_mission_model_user_admin: tuple[CommunityModel, MissionModel, CommunityMissionModel],
) -> AsyncGenerator[MissionCommunity, None]:
    _, _, community_mission = test_community_mission_model_user_admin
    community_mission.status = OccupancyStatusEnum.FINISH
    session.add(community_mission)
    await session.commit()
    yield MissionCommunity(
        id=community_mission.id,
        community_id=community_mission.community_id,
        mission_id=community_mission.mission_id,
        author=community_mission.author,
        date_start=community_mission.date_start,
        date_close=community_mission.date_close,
        status=community_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_no_user_entity(
    test_community_mission_model_no_user: tuple[CommunityModel, MissionModel, CommunityMissionModel]
) -> AsyncGenerator[MissionCommunity, None]:
    _, _, community_mission = test_community_mission_model_no_user
    yield MissionCommunity(
        id=community_mission.id,
        community_id=community_mission.community_id,
        mission_id=community_mission.mission_id,
        author=community_mission.author,
        date_start=community_mission.date_start,
        date_close=community_mission.date_close,
        status=community_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_user_blocked_entity(
    test_community_mission_model_user_blocked: tuple[CommunityModel, MissionModel, CommunityMissionModel]
) -> AsyncGenerator[MissionCommunity, None]:
    _, _, community_mission = test_community_mission_model_user_blocked
    yield MissionCommunity(
        id=community_mission.id,
        community_id=community_mission.community_id,
        mission_id=community_mission.mission_id,
        author=community_mission.author,
        date_start=community_mission.date_start,
        date_close=community_mission.date_close,
        status=community_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_community_mission_not_active_community_entity(
    test_community_mission_model_no_active_community: tuple[CommunityModel, MissionModel, CommunityMissionModel]
) -> AsyncGenerator[MissionCommunity, None]:
    _, _, community_mission = test_community_mission_model_no_active_community
    yield MissionCommunity(
        id=community_mission.id,
        community_id=community_mission.community_id,
        mission_id=community_mission.mission_id,
        author=community_mission.author,
        date_start=community_mission.date_start,
        date_close=community_mission.date_close,
        status=community_mission.status,
    )


@pytest_asyncio.fixture(scope="function")
async def test_user_community_user_dto(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_community_model_public: CommunityModel,
) -> AsyncGenerator[UserCommunityDTO, None]:
    user_community = UserCommunityModel(
        user_id=test_user_model_ru.id,
        community_id=test_community_model_public.id,
        role=CommunityRoleEnum.USER,
    )
    session.add(user_community)
    await session.commit()

    yield UserCommunityDTO(
        user_id=user_community.user_id,
        community_id=user_community.community_id,
        role=user_community.role,
    )

    await session.delete(user_community)
    await session.commit()


@pytest_asyncio.fixture(scope="function")
async def test_user_community_admin_dto(
    session: AsyncSession,
    test_user_model_ru: UserModel,
    test_community_model_public: CommunityModel,
) -> AsyncGenerator[UserCommunityDTO, None]:
    user_community = UserCommunityModel(
        user_id=test_user_model_ru.id,
        community_id=test_community_model_public.id,
        role=CommunityRoleEnum.ADMIN,
    )
    session.add(user_community)
    await session.commit()

    yield UserCommunityDTO(
        user_id=user_community.user_id,
        community_id=user_community.community_id,
        role=user_community.role,
    )

    await session.delete(user_community)
    await session.commit()
