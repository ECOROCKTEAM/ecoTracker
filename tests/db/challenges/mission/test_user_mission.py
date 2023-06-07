from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionUserCreateDTO, MissionUserUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.mission import (
    MissionFilter,
    MissionUserFilter,
)
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.models.challenges.mission import UserMissionModel
from src.data.models.user.user import UserModel
from src.data.repository.challenges.mission import RepositoryMission


# python -m pytest tests/db/challenges/mission/test_user_mission.py::test_get_user_mission_ok -v -s
@pytest.mark.asyncio
async def test_get_user_mission_ok(repo: RepositoryMission, test_user_mission_entity: MissionUser):
    user_mission = await repo.user_mission_get(id=test_user_mission_entity.id, user_id=test_user_mission_entity.user_id)
    assert test_user_mission_entity.id == user_mission.id
    assert test_user_mission_entity.user_id == user_mission.user_id
    assert test_user_mission_entity.mission_id == user_mission.mission_id
    assert test_user_mission_entity.date_start == user_mission.date_start
    assert test_user_mission_entity.date_close == user_mission.date_close
    assert test_user_mission_entity.status == user_mission.status


# python -m pytest tests/db/challenges/mission/test_user_mission.py::test_get_user_mission_not_found -v -s
@pytest.mark.asyncio
async def test_get_user_mission_not_found(repo: RepositoryMission):
    with pytest.raises(EntityNotFound):
        _ = await repo.user_mission_get(id=-1, user_id=1)


# python -m pytest tests/db/challenges/mission/test_user_mission.py::test_create_user_mission_ok -v -s
@pytest.mark.asyncio
async def test_create_user_mission_ok(
    session: AsyncSession, repo: RepositoryMission, test_user_model: UserModel, test_mission_entity_ru: Mission
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_mission_list = await repo.user_mission_lst(
        user_id=test_user_model.id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 0
    user_mission = await repo.user_mission_create(
        user_id=test_user_model.id,
        obj=MissionUserCreateDTO(
            mission_id=test_mission_entity_ru.id,
        ),
    )
    await session.commit()
    assert user_mission.id is not None
    assert user_mission.user_id == test_user_model.id
    assert user_mission.mission_id == test_mission_entity_ru.id
    assert isinstance(user_mission.date_start, datetime)
    assert user_mission.date_close is None
    assert user_mission.status == OccupancyStatusEnum.ACTIVE

    user_mission_list = await repo.user_mission_lst(
        user_id=test_user_model.id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 1

    create_model = await session.get(entity=UserMissionModel, ident={"id": user_mission.id})
    assert isinstance(create_model, UserMissionModel)
    await session.delete(create_model)
    await session.commit()


# python -m pytest tests/db/challenges/mission/test_user_mission.py::test_create_user_mission_not_created -v -s
@pytest.mark.asyncio
async def test_create_user_mission_not_created(
    session: AsyncSession,
    repo: RepositoryMission,
    test_user_model: UserModel,
    test_mission_entity_ru: Mission,
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_mission_list = await repo.user_mission_lst(
        user_id=test_user_model.id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 0
    with pytest.raises(EntityNotCreated):
        _ = await repo.user_mission_create(
            user_id=-1,
            obj=MissionUserCreateDTO(
                mission_id=test_mission_entity_ru.id,
            ),
        )
    await session.rollback()
    await session.refresh(test_user_model)
    user_mission_list = await repo.user_mission_lst(
        user_id=test_user_model.id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 0


# python -m pytest tests/db/challenges/mission/test_user_mission.py::test_update_user_mission -v -s
@pytest.mark.asyncio
async def test_update_user_mission(
    session: AsyncSession,
    repo: RepositoryMission,
    test_user_mission_entity: MissionUser,
):
    assert test_user_mission_entity.status == OccupancyStatusEnum.ACTIVE
    assert test_user_mission_entity.date_close is None

    updated = await repo.user_mission_update(
        id=test_user_mission_entity.id,
        user_id=test_user_mission_entity.user_id,
        obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    await session.commit()

    assert isinstance(updated.date_close, datetime)
    assert updated.status == OccupancyStatusEnum.FINISH

    date_after_update = updated.date_close

    updated_second = await repo.user_mission_update(
        id=test_user_mission_entity.id,
        user_id=test_user_mission_entity.user_id,
        obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.REJECT),
    )
    await session.commit()

    assert isinstance(updated_second.date_close, datetime)
    assert updated_second.status == OccupancyStatusEnum.REJECT
    assert updated_second.date_close > date_after_update


# python -m pytest tests/db/challenges/mission/test_user_mission.py::test_update_user_mission_not_found -v -s
@pytest.mark.asyncio
async def test_update_user_mission_not_found(
    repo: RepositoryMission,
    test_user_mission_entity: MissionUser,
):
    with pytest.raises(EntityNotFound):
        _ = await repo.user_mission_update(
            id=-1, user_id=test_user_mission_entity.user_id, obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )
    with pytest.raises(EntityNotFound):
        _ = await repo.user_mission_update(
            id=test_user_mission_entity.id, user_id=-1, obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )

    with pytest.raises(EntityNotFound):
        _ = await repo.user_mission_update(
            id=-1, user_id=-1, obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )


# python -m pytest tests/db/challenges/mission/test_user_mission.py::test_user_mission_lst -v -s
@pytest.mark.asyncio
async def test_user_mission_lst(repo: RepositoryMission, test_user_mission_entity: MissionUser):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_mission_list = await repo.user_mission_lst(
        user_id=test_user_mission_entity.user_id,
        filter_obj=MissionUserFilter(mission_id=test_user_mission_entity.mission_id, status=OccupancyStatusEnum.ACTIVE),
        **default_kw,
    )
    assert len(user_mission_list) == 1

    user_mission = user_mission_list[0]

    assert user_mission.id is not None
    assert user_mission.user_id == test_user_mission_entity.user_id
    assert user_mission.mission_id == test_user_mission_entity.mission_id
    assert user_mission.status == OccupancyStatusEnum.ACTIVE

    user_mission_list = await repo.user_mission_lst(
        user_id=test_user_mission_entity.user_id, filter_obj=MissionUserFilter(), **default_kw
    )
    assert len(user_mission_list) == 1

    user_mission_list = await repo.user_mission_lst(
        user_id=test_user_mission_entity.user_id, filter_obj=MissionUserFilter(mission_id=-1), **default_kw
    )
    assert len(user_mission_list) == 0

    user_mission_list = await repo.user_mission_lst(
        user_id=test_user_mission_entity.user_id,
        filter_obj=MissionUserFilter(status=OccupancyStatusEnum.FINISH),
        **default_kw,
    )
    assert len(user_mission_list) == 0
