from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.challenges.mission import MissionGroupCreateDTO, MissionGroupUpdateDTO
from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.entity.mission import Mission, MissionGroup
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.challenges.mission import MissionGroupFilter
from src.data.models.challenges.mission import GroupMissionModel
from src.data.models.group.group import GroupModel
from src.data.repository.challenges.mission import RepositoryMission
from tests.fixtures.challenges.category.db.model import fxm_category_default
from tests.fixtures.challenges.mission.db.entity import fxe_mission_default
from tests.fixtures.challenges.mission.db.group.entity import fxe_group_mission_default
from tests.fixtures.challenges.mission.db.group.model import fxm_group_mission_default
from tests.fixtures.challenges.mission.db.model import fxm_mission_default
from tests.fixtures.group.db.entity import fxe_group_default
from tests.fixtures.group.db.model import fxm_group_default
from tests.fixtures.group.db.user.model import fxm_user_group_default
from tests.fixtures.user.db.model import fxm_user_default


# pytest tests/main/challenges/mission/db/test_group_mission.py::test_get_group_mission_ok -v -s
@pytest.mark.asyncio
async def test_get_group_mission_ok(repo: RepositoryMission, fxe_group_mission_default: MissionGroup):
    mission = await repo.group_mission_get(id=fxe_group_mission_default.id, group_id=fxe_group_mission_default.group_id)

    assert fxe_group_mission_default.id == mission.id
    assert fxe_group_mission_default.group_id == mission.group_id
    assert fxe_group_mission_default.mission_id == mission.mission_id
    assert fxe_group_mission_default.author == mission.author
    assert fxe_group_mission_default.date_start == mission.date_start
    assert fxe_group_mission_default.date_close == mission.date_close
    assert fxe_group_mission_default.status == mission.status


# pytest tests/main/challenges/mission/db/test_group_mission.py::test_get_group_mission_not_found -v -s
@pytest.mark.asyncio
async def test_get_group_mission_not_found(repo: RepositoryMission):
    with pytest.raises(EntityNotFound):
        _ = await repo.group_mission_get(id=-1, group_id=1)


# pytest tests/main/challenges/mission/db/test_group_mission.py::test_create_group_mission_ok -v -s
@pytest.mark.asyncio
async def test_create_group_mission_ok(
    session: AsyncSession,
    repo: RepositoryMission,
    fxe_group_default: Group,
    fxe_mission_default: Mission,
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    group_mission_list = await repo.group_mission_lst(filter_obj=MissionGroupFilter(), **default_kw)
    assert len(group_mission_list) == 0

    group_mission = await repo.group_mission_create(
        group_id=fxe_group_default.id,
        obj=MissionGroupCreateDTO(mission_id=fxe_mission_default.id, author="t"),
    )
    assert group_mission.id is not None
    assert group_mission.mission_id == fxe_mission_default.id
    assert group_mission.group_id == fxe_group_default.id
    assert group_mission.author == "t"
    assert group_mission.status == OccupancyStatusEnum.ACTIVE
    assert isinstance(group_mission.date_start, datetime)
    assert group_mission.date_close is None

    create_model = await session.get(entity=GroupMissionModel, ident={"id": group_mission.id})
    assert isinstance(create_model, GroupMissionModel)
    await session.delete(create_model)
    await session.commit()


# pytest tests/main/challenges/mission/db/test_group_mission.py::test_create_group_mission_not_created -v -s
@pytest.mark.asyncio
async def test_create_group_mission_not_created(
    session: AsyncSession,
    repo: RepositoryMission,
    fxe_group_default: Group,
    fxe_mission_default: Mission,
):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    group_mission_list = await repo.group_mission_lst(filter_obj=MissionGroupFilter(), **default_kw)
    assert len(group_mission_list) == 0
    with pytest.raises(EntityNotCreated):
        _ = await repo.group_mission_create(
            group_id=-1, obj=MissionGroupCreateDTO(mission_id=fxe_mission_default.id, author="t")
        )
    await session.rollback()
    with pytest.raises(EntityNotCreated):
        _ = await repo.group_mission_create(
            group_id=fxe_group_default.id, obj=MissionGroupCreateDTO(mission_id=-1, author="t")
        )
    await session.rollback()

    group_mission_list = await repo.group_mission_lst(filter_obj=MissionGroupFilter(), **default_kw)
    assert len(group_mission_list) == 0


# pytest tests/main/challenges/mission/db/test_group_mission.py::test_update_group_mission_ok -v -s
@pytest.mark.asyncio
async def test_update_group_mission_ok(
    session: AsyncSession,
    repo: RepositoryMission,
    fxe_group_mission_default: MissionGroup,
):
    assert fxe_group_mission_default.date_close is None

    updated = await repo.group_mission_update(
        id=fxe_group_mission_default.id,
        group_id=fxe_group_mission_default.group_id,
        obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.FINISH),
    )
    await session.commit()

    assert isinstance(updated.date_close, datetime)
    assert updated.status == OccupancyStatusEnum.FINISH

    date_after_update = updated.date_close

    updated_second = await repo.group_mission_update(
        id=fxe_group_mission_default.id,
        group_id=fxe_group_mission_default.group_id,
        obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.REJECT),
    )
    await session.commit()

    assert isinstance(updated_second.date_close, datetime)
    assert updated_second.status == OccupancyStatusEnum.REJECT
    assert updated_second.date_close > date_after_update


# pytest tests/main/challenges/mission/db/test_group_mission.py::test_update_group_mission_not_found -v -s
@pytest.mark.asyncio
async def test_update_group_mission_not_found(
    repo: RepositoryMission,
    fxe_group_mission_default: MissionGroup,
):
    with pytest.raises(EntityNotFound):
        _ = await repo.group_mission_update(
            id=-1,
            group_id=fxe_group_mission_default.group_id,
            obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )
    with pytest.raises(EntityNotFound):
        _ = await repo.group_mission_update(
            id=fxe_group_mission_default.id,
            group_id=-1,
            obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.FINISH),
        )

    with pytest.raises(EntityNotFound):
        _ = await repo.group_mission_update(
            id=-1, group_id=-1, obj=MissionGroupUpdateDTO(status=OccupancyStatusEnum.FINISH)
        )


# pytest tests/main/challenges/mission/db/test_group_mission.py::test_group_mission_lst -v -s
@pytest.mark.asyncio
async def test_group_mission_lst(repo: RepositoryMission, fxe_group_mission_default: MissionGroup):
    default_kw = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    group_mission_list = await repo.group_mission_lst(
        filter_obj=MissionGroupFilter(
            group_id_list=[fxe_group_mission_default.group_id],
            group_id=fxe_group_mission_default.group_id,
            status=OccupancyStatusEnum.ACTIVE,
        ),
        **default_kw,
    )
    assert len(group_mission_list) == 1

    group_mission = group_mission_list[0]

    assert group_mission.id is not None
    assert group_mission.group_id == fxe_group_mission_default.group_id
    assert group_mission.mission_id == fxe_group_mission_default.mission_id
    assert group_mission.status == OccupancyStatusEnum.ACTIVE

    group_mission_list = await repo.group_mission_lst(
        filter_obj=MissionGroupFilter(),
        **default_kw,
    )
    assert len(group_mission_list) == 1

    group_mission_list = await repo.group_mission_lst(
        filter_obj=MissionGroupFilter(mission_id=-1),
        **default_kw,
    )
    assert len(group_mission_list) == 0

    group_mission_list = await repo.group_mission_lst(
        filter_obj=MissionGroupFilter(group_id=-1),
        **default_kw,
    )
    assert len(group_mission_list) == 0

    group_mission_list = await repo.group_mission_lst(
        filter_obj=MissionGroupFilter(group_id_list=[]),
        **default_kw,
    )
    assert len(group_mission_list) == 0
