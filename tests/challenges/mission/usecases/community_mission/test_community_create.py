import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionCommunityCreateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionCommunity
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotActive, EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionCommunityFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_community_create import (
    MissionCommunityCreateUsecase,
)
from src.data.models.challenges.mission import CommunityMissionModel
from src.data.models.community.community import CommunityModel


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_create.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    session: AsyncSession,
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_user_community_admin_dto: UserCommunityDTO,
    test_mission_entity_ru: Mission,
):
    assert test_user_premium_ru_entity.id == test_user_community_admin_dto.user_id
    uc = MissionCommunityCreateUsecase(uow=uow)
    res = await uc(
        user=test_user_premium_ru_entity,
        community_id=test_user_community_admin_dto.community_id,
        create_obj=MissionCommunityCreateDTO(
            mission_id=test_mission_entity_ru.id,
            author=test_user_premium_ru_entity.username,
        ),
    )
    mission = res.item
    assert isinstance(mission, MissionCommunity)
    assert mission.id is not None
    assert mission.community_id == test_user_community_admin_dto.community_id
    assert mission.mission_id == test_mission_entity_ru.id
    assert mission.status == OccupancyStatusEnum.ACTIVE
    assert mission.author == test_user_premium_ru_entity.username

    async with uow as _uow:
        community_mission_list = await _uow.mission.community_mission_lst(
            filter_obj=MissionCommunityFilter(),
            order_obj=MockObj(),
            pagination_obj=MockObj(),
        )
        assert len(community_mission_list) == 1

    create_model = await session.get(entity=CommunityMissionModel, ident={"id": mission.id})
    assert isinstance(create_model, CommunityMissionModel)
    await session.delete(create_model)
    await session.commit()


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_create.py::test_user_not_in_community -v -s
@pytest.mark.asyncio
async def test_user_not_in_community(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_community_model_public: CommunityModel,
    test_mission_entity_ru: Mission,
):
    uc = MissionCommunityCreateUsecase(uow=uow)
    with pytest.raises(EntityNotFound):
        await uc(
            user=test_user_premium_ru_entity,
            community_id=test_community_model_public.id,
            create_obj=MissionCommunityCreateDTO(
                mission_id=test_mission_entity_ru.id,
                author=test_user_premium_ru_entity.username,
            ),
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_create.py::test_user_incorrect_role -v -s
@pytest.mark.asyncio
async def test_user_incorrect_role(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_user_community_user_dto: UserCommunityDTO,
    test_mission_entity_ru: Mission,
):
    uc = MissionCommunityCreateUsecase(uow=uow)
    with pytest.raises(PermissionError):
        await uc(
            user=test_user_premium_ru_entity,
            community_id=test_user_community_user_dto.community_id,
            create_obj=MissionCommunityCreateDTO(
                mission_id=test_mission_entity_ru.id,
                author=test_user_premium_ru_entity.username,
            ),
        )


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_create.py::test_mission_not_active -v -s
@pytest.mark.asyncio
async def test_mission_not_active(
    uow: IUnitOfWork,
    test_user_premium_ru_entity: User,
    test_user_community_admin_dto: UserCommunityDTO,
    test_mission_entity_not_active: Mission,
):
    uc = MissionCommunityCreateUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        await uc(
            user=test_user_premium_ru_entity,
            community_id=test_user_community_admin_dto.community_id,
            create_obj=MissionCommunityCreateDTO(
                mission_id=test_mission_entity_not_active.id,
                author=test_user_premium_ru_entity.username,
            ),
        )
