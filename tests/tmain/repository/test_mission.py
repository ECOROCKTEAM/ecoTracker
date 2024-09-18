from datetime import datetime

import pytest

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.challenges.mission import (
    MissionGroupCreateDTO,
    MissionGroupUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.utils import IterableObj
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.mission import (
    IRepositoryMission,
    MissionFilter,
    MissionGroupFilter,
    MissionUserFilter,
    SortGroupMissionObj,
    SortMissionObj,
    SortUserMissionObj,
)
from src.data.models.user.user import UserModel
from tests.dataloader import dataloader


# pytest tests/tmain/repository/test_mission.py::test_mission_get_ok -v -s
@pytest.mark.asyncio
async def test_mission_get_ok(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    mission = await dl.create_mission()
    await dl.create_mission()

    # Act
    res = await repo_mission.get(id=mission.id, lang=LanguageEnum.EN)

    # Assert
    assert res.id == mission.id
    assert res.active == mission.active
    assert res.category_id == mission.category_id
    assert res.language == LanguageEnum.EN


# pytest tests/tmain/repository/test_mission.py::test_mission_get_translate_is_none_get_default -v -s
@pytest.mark.asyncio
async def test_mission_get_translate_is_none_get_default(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    mission = await dl.create_mission(language_list=[DEFAULT_LANGUANGE, LanguageEnum.RU])
    await dl.create_mission()

    # Act
    res = await repo_mission.get(id=mission.id, lang=LanguageEnum.FR)

    # Assert
    assert res.id == mission.id
    assert res.active == mission.active
    assert res.category_id == mission.category_id
    assert res.language == DEFAULT_LANGUANGE


# pytest tests/tmain/repository/test_mission.py::test_mission_get_translate_is_none -v -s
@pytest.mark.asyncio
async def test_mission_get_translate_is_none(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    mission = await dl.create_mission(language_list=[LanguageEnum.FR])
    await dl.create_mission(language_list=[lang for lang in LanguageEnum])

    # Act
    with pytest.raises(TranslateNotFound) as e:
        await repo_mission.get(id=mission.id, lang=LanguageEnum.RU)

    # Assert
    assert f"Translate for mission id={mission.id} not found" in str(e.value)


# pytest tests/tmain/repository/test_mission.py::test_mission_get_not_found_error -v -s
@pytest.mark.asyncio
async def test_mission_get_not_found_error(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    await dl.create_mission()
    mission_id_not_exist = -1

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_mission.get(id=mission_id_not_exist, lang=DEFAULT_LANGUANGE)

    # Assert
    assert f"Mission id={mission_id_not_exist} not found" in str(e.value)


async def _arrange_mission_list_filter_empty(dl: dataloader) -> tuple[set[int], MissionFilter]:
    mission_id_set = set()
    mission_1 = await dl.create_mission()
    mission_2 = await dl.create_mission()
    mission_3 = await dl.create_mission()
    mission_id_set.update([mission_1.id, mission_2.id, mission_3.id])

    filter_obj = MissionFilter()
    return mission_id_set, filter_obj


async def _arrange_mission_list_filter_active_true(dl: dataloader) -> tuple[set[int], MissionFilter]:
    mission_id_set = set()
    mission_1 = await dl.create_mission(active=True)
    mission_2 = await dl.create_mission(active=True)
    mission_3 = await dl.create_mission(active=True)
    mission_4 = await dl.create_mission(active=False)
    mission_id_set.update([mission_1.id, mission_2.id, mission_3.id, mission_4.id])

    filter_obj = MissionFilter(active=True)
    return mission_id_set, filter_obj


# pytest tests/tmain/repository/test_mission.py::test_mission_list_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize("arrange_func", [_arrange_mission_list_filter_empty, _arrange_mission_list_filter_active_true])
async def test_mission_list_ok(dl: dataloader, repo_mission: IRepositoryMission, arrange_func):
    # Arrange
    arrange_mission_id_set, filter_obj = await arrange_func(dl=dl)

    # Act
    mission_list = await repo_mission.lst(
        filter_obj=filter_obj, sorting_obj=SortMissionObj(), iterable_obj=IterableObj(), lang=DEFAULT_LANGUANGE
    )

    # Assert
    assert len(mission_list.items) == len(arrange_mission_id_set)


async def _arrange_mission_pagination_list_offet_0_limit_5(dl: dataloader) -> tuple[int, int, int, int | None]:
    await dl.create_mission_list_random(count=20)
    return 20, 5, 0, 5


async def _arrange_mission_pagination_list_offet_10_limit_5(dl: dataloader) -> tuple[int, int, int, int | None]:
    await dl.create_mission_list_random(count=20)
    return 20, 5, 10, 5


async def _arrange_mission_pagination_list_offet_5_limit_none(dl: dataloader) -> tuple[int, int, int, int | None]:
    await dl.create_mission_list_random(count=20)
    return 20, 15, 5, None


async def _arrange_mission_pagination_list_offet_19_limit_none(dl: dataloader) -> tuple[int, int, int, int | None]:
    await dl.create_mission_list_random(count=20)
    return 20, 1, 19, None


# pytest tests/tmain/repository/test_mission.py::test_mission_lst_paggination -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _arrange_mission_pagination_list_offet_0_limit_5,
        _arrange_mission_pagination_list_offet_10_limit_5,
        _arrange_mission_pagination_list_offet_19_limit_none,
        _arrange_mission_pagination_list_offet_5_limit_none,
    ],
)
async def test_mission_lst_paggination(dl: dataloader, repo_mission: IRepositoryMission, arrange_func):
    # Arrange
    total, count, arrange_offset, arrange_limit = await arrange_func(dl=dl)

    # Act
    mission_list = await repo_mission.lst(
        filter_obj=MissionFilter(),
        sorting_obj=SortMissionObj(),
        iterable_obj=IterableObj(limit=arrange_limit, offset=arrange_offset),
        lang=DEFAULT_LANGUANGE,
    )

    # Assert
    assert len(mission_list.items) == count
    assert mission_list.total == total
    assert mission_list.offset == arrange_offset
    assert mission_list.limit == arrange_limit


# pytest tests/tmain/repository/test_mission.py::test_mission_list_translate_not_found_error -v -s
@pytest.mark.asyncio
async def test_mission_list_translate_not_found_error(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    category = await dl.create_category()
    mission_without_translate = await dl.mission_loader.create(category=category)
    await dl.create_mission()

    # Act
    with pytest.raises(TranslateNotFound) as e:
        await repo_mission.lst(
            filter_obj=MissionFilter(), sorting_obj=SortMissionObj(), iterable_obj=IterableObj(), lang=DEFAULT_LANGUANGE
        )

    # Assert
    assert f"{mission_without_translate.id=}, {DEFAULT_LANGUANGE=}"


# pytest tests/tmain/repository/test_mission.py::test_user_mission_get_ok -v -s
@pytest.mark.asyncio
async def test_user_mission_get_ok(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    user_mission = await dl.create_user_mission(user=user)
    await dl.create_user_mission(user=user)

    # Act
    res = await repo_mission.user_mission_get(id=user_mission.id, user_id=user.id)

    # Assert
    assert res.id == user_mission.id
    assert res.user_id == user_mission.user_id == user.id
    assert res.mission_id == user_mission.mission_id
    assert res.status == user_mission.status
    assert isinstance(res.date_start, datetime)


# pytest tests/tmain/repository/test_mission.py::test_user_mission_get_not_exist_error -v -s
@pytest.mark.asyncio
async def test_user_mission_get_not_exist_error(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    await dl.create_user_mission(user=user)
    not_exist_id = -1

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_mission.user_mission_get(id=not_exist_id, user_id=user.id)

    # Assert
    assert f"id={not_exist_id}" in str(e.value)


# pytest tests/tmain/repository/test_mission.py::test_user_mission_create_ok -v -s
@pytest.mark.asyncio
async def test_user_mission_create_ok(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    mission = await dl.create_mission()
    await dl.create_mission()

    create_obj = MissionUserCreateDTO(mission_id=mission.id, status=OccupancyStatusEnum.ACTIVE)

    # Act
    res = await repo_mission.user_mission_create(user_id=user.id, obj=create_obj)

    # Assert
    assert res.mission_id == mission.id
    assert res.user_id == user.id
    assert isinstance(res.date_start, datetime)
    assert res.status == create_obj.status


# pytest tests/tmain/repository/test_mission.py::test_user_mission_create_not_found_fk_error -v -s
@pytest.mark.asyncio
async def test_user_mission_create_not_found_fk_error(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    await dl.create_mission()

    create_obj = MissionUserCreateDTO(mission_id=-1, status=OccupancyStatusEnum.ACTIVE)

    # Act
    with pytest.raises(EntityNotCreated) as e:
        await repo_mission.user_mission_create(user_id=user.id, obj=create_obj)

    # Assert
    assert "Not found fk" in str(e.value)


# pytest tests/tmain/repository/test_mission.py::test_user_mission_update_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_update_obj",
    [
        MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH),
        MissionUserUpdateDTO(status=OccupancyStatusEnum.OVERDUE),
        MissionUserUpdateDTO(status=OccupancyStatusEnum.REJECT),
    ],
)
async def test_user_mission_update_ok(
    dl: dataloader, repo_mission: IRepositoryMission, arrange_update_obj: MissionUserUpdateDTO
):
    # Arrange
    user = await dl.user_loader.create()
    user_mission = await dl.create_user_mission(user=user, status=OccupancyStatusEnum.ACTIVE)
    await dl.create_user_mission(user=user)

    status_date_close_set = {OccupancyStatusEnum.FINISH, OccupancyStatusEnum.REJECT}

    # Act
    res = await repo_mission.user_mission_update(id=user_mission.id, user_id=user.id, obj=arrange_update_obj)

    # Assert
    assert res.id == user_mission.id
    assert res.mission_id == user_mission.mission_id
    assert res.user_id == user_mission.user_id
    assert isinstance(res.date_start, datetime)
    if res.status in status_date_close_set:
        assert isinstance(res.date_close, datetime)
    else:
        assert isinstance(res.date_close, type(None))


# pytest tests/tmain/repository/test_mission.py::test_user_mission_update_not_found_fk -v -s
@pytest.mark.asyncio
async def test_user_mission_update_not_found_fk(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    await dl.create_user_mission(user=user)
    not_exist_id = -1

    update_obj = MissionUserUpdateDTO(status=OccupancyStatusEnum.REJECT)

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_mission.user_mission_update(id=not_exist_id, user_id=user.id, obj=update_obj)

    # Assert
    assert f"Not found id={not_exist_id}" in str(e.value)


async def _arrange_user_mission_filter_mission_id(
    dl: dataloader, user: UserModel
) -> tuple[set[int], MissionUserFilter]:
    mission = await dl.create_mission()
    mission_fictitious = await dl.create_mission()

    user_mission_1 = await dl.create_user_mission(user=user, mission=mission)
    user_mission_2 = await dl.create_user_mission(user=user, mission=mission)
    user_mission_3 = await dl.create_user_mission(user=user, mission=mission)
    await dl.create_user_mission(user=user, mission=mission_fictitious)
    await dl.create_user_mission(user=user, mission=mission_fictitious)

    filter_obj = MissionUserFilter(mission_id=mission.id)
    user_mission_id_set = {user_mission_1.id, user_mission_2.id, user_mission_3.id}
    return user_mission_id_set, filter_obj


async def _arrange_user_mission_filter_status(dl: dataloader, user: UserModel) -> tuple[set[int], MissionUserFilter]:
    mission = await dl.create_mission()

    user_mission_1 = await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.ACTIVE)
    user_mission_2 = await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.ACTIVE)
    await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.FINISH)
    await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.OVERDUE)
    await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.REJECT)

    filter_obj = MissionUserFilter(status=OccupancyStatusEnum.ACTIVE)
    user_mission_id_set = {user_mission_1.id, user_mission_2.id}
    return user_mission_id_set, filter_obj


async def _arrange_user_mission_filter_empty(dl: dataloader, user: UserModel) -> tuple[set[int], MissionUserFilter]:
    mission = await dl.create_mission()

    user_mission_1 = await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.ACTIVE)
    user_mission_2 = await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.FINISH)
    user_mission_3 = await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.OVERDUE)
    user_mission_4 = await dl.create_user_mission(user=user, mission=mission, status=OccupancyStatusEnum.REJECT)

    filter_obj = MissionUserFilter()
    user_mission_id_set = {user_mission_1.id, user_mission_2.id, user_mission_3.id, user_mission_4.id}
    return user_mission_id_set, filter_obj


# pytest tests/tmain/repository/test_mission.py::test_user_mission_list_filter -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [_arrange_user_mission_filter_mission_id, _arrange_user_mission_filter_status, _arrange_user_mission_filter_empty],
)
async def test_user_mission_list_filter(dl: dataloader, repo_mission: IRepositoryMission, arrange_func):
    # Arrange
    user = await dl.user_loader.create()
    arrange_user_mission_set_id, filter_obj = await arrange_func(dl=dl, user=user)

    # Act
    res = await repo_mission.user_mission_lst(
        user_id=user.id, filter_obj=filter_obj, sorting_obj=SortUserMissionObj(), iterable_obj=IterableObj()
    )
    res_user_mission_id_set = {user_mission.id for user_mission in res.items}
    res_user_mission_status_set = {user_mission.status for user_mission in res.items}

    # Assert
    assert arrange_user_mission_set_id == res_user_mission_id_set
    if filter_obj.status is not None:
        assert res_user_mission_status_set == set([filter_obj.status])
    if filter_obj.mission_id is not None:
        res_mission_id_set = {user_mission.mission_id for user_mission in res.items}
        assert res_mission_id_set == set([filter_obj.mission_id])


async def _arrange_user_mission_paggination_offset_10_limit_5(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_mission_list_random(user=user, count=20)
    return 20, 3, 17, 5


async def _arrange_user_mission_paggination_offset_5_limit_none(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_mission_list_random(user=user, count=20)
    return 20, 15, 5, None


async def _arrange_user_mission_paggination_offset_19_limit_none(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_mission_list_random(user=user, count=20)
    return 20, 1, 19, None


async def _arrange_user_mission_paggination_offset_10_limit_none(
    dl: dataloader, user: UserModel
) -> tuple[int, int, int, int | None]:
    await dl.create_user_mission_list_random(user=user, count=20)
    return 20, 10, 10, None


# pytest tests/tmain/repository/test_mission.py::test_user_mission_pagination -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _arrange_user_mission_paggination_offset_10_limit_5,
        _arrange_user_mission_paggination_offset_5_limit_none,
        _arrange_user_mission_paggination_offset_19_limit_none,
        _arrange_user_mission_paggination_offset_10_limit_none,
    ],
)
async def test_user_mission_pagination(dl: dataloader, repo_mission: IRepositoryMission, arrange_func):
    # Arrange
    user = await dl.user_loader.create()
    total, arrange_count, arrange_offset, arrange_limit = await arrange_func(dl=dl, user=user)

    # Act
    res = await repo_mission.user_mission_lst(
        user_id=user.id,
        filter_obj=MissionUserFilter(),
        sorting_obj=SortUserMissionObj(),
        iterable_obj=IterableObj(limit=arrange_limit, offset=arrange_offset),
    )

    # Assert
    assert res.limit == arrange_limit
    assert res.offset == arrange_offset
    assert len(res.items) == arrange_count
    assert res.total == total


# pytest tests/tmain/repository/test_mission.py::test_group_mission_create_ok -v -s
@pytest.mark.asyncio
async def test_group_mission_create_ok(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    mission = await dl.create_mission()
    group = await dl.group_loader.create()

    create_obj = MissionGroupCreateDTO(
        mission_id=mission.id,
        author=user.id,
        place="Genova",
        meeting_date=datetime.now(),
        people_required=15,
        people_max=30,
        comment="Desc mission text",
    )

    # Act
    res = await repo_mission.group_mission_create(group_id=group.id, obj=create_obj)

    # Assert
    assert res.author == user.id
    assert res.mission_id == mission.id
    assert res.group_id == group.id
    assert isinstance(res.comment, str)
    assert isinstance(res.meeting_date, datetime)
    assert isinstance(res.date_start, datetime)
    assert isinstance(res.people_max, int)
    assert isinstance(res.people_required, int)


# pytest tests/tmain/repository/test_mission.py::test_group_mission_create_mission_not_exist_error -v -s
@pytest.mark.asyncio
async def test_group_mission_create_mission_not_exist_error(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    mission_not_exist_id = -1

    create_obj = MissionGroupCreateDTO(
        mission_id=mission_not_exist_id,
        author=user.id,
        place="Genova",
        meeting_date=datetime.now(),
        people_required=15,
        people_max=30,
        comment="Desc mission text",
    )

    # Act
    with pytest.raises(EntityNotCreated) as e:
        await repo_mission.group_mission_create(group_id=group.id, obj=create_obj)
    # Assert
    assert "Not found fk" in str(e.value)


# pytest tests/tmain/repository/test_mission.py::test_group_mission_create_group_not_exist_error -v -s
@pytest.mark.asyncio
async def test_group_mission_create_group_not_exist_error(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    mission = await dl.create_mission()
    group_not_exist_id = -1

    create_obj = MissionGroupCreateDTO(
        mission_id=mission.id,
        author=user.id,
        place="Genova",
        meeting_date=datetime.now(),
        people_required=15,
        people_max=30,
        comment="Desc mission text",
    )

    # Act
    with pytest.raises(EntityNotCreated) as e:
        await repo_mission.group_mission_create(group_id=group_not_exist_id, obj=create_obj)
    # Assert
    assert "Not found fk" in str(e.value)


# pytest tests/tmain/repository/test_mission.py::test_group_mission_get_ok -v -s
@pytest.mark.asyncio
async def test_group_mission_get_ok(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    mission = await dl.create_mission()

    group_mission = await dl.create_group_mission(user=user, group=group, mission=mission)
    await dl.create_group_mission(user=user, group=group)

    # Act
    res = await repo_mission.group_mission_get(id=group_mission.id, group_id=group.id)

    # Assert
    assert res.author == user.id
    assert res.mission_id == mission.id
    assert res.group_id == group.id


# pytest tests/tmain/repository/test_mission.py::test_group_mission_get_entity_not_found_error -v -s
@pytest.mark.asyncio
async def test_group_mission_get_entity_not_found_error(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    mission = await dl.create_mission()
    group_mission_not_exist_id = -1

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_mission.group_mission_get(id=group_mission_not_exist_id, group_id=group.id)
    # Assert
    assert f"id={group_mission_not_exist_id}, group_id={group.id}" in str(e.value)


# pytest tests/tmain/repository/test_mission.py::test_group_mission_update_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_status", [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.OVERDUE, OccupancyStatusEnum.REJECT]
)
async def test_group_mission_update_ok(
    dl: dataloader, repo_mission: IRepositoryMission, arrange_status: OccupancyStatusEnum
):
    # Arrange
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    mission = await dl.create_mission()

    group_mission = await dl.create_group_mission(
        user=user, group=group, mission=mission, status=OccupancyStatusEnum.ACTIVE
    )
    await dl.create_group_mission(user=user, group=group, mission=mission)

    update_obj = MissionGroupUpdateDTO(status=arrange_status)
    date_close_status_list = [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.REJECT]

    # Act
    res = await repo_mission.group_mission_update(id=group_mission.id, group_id=group.id, obj=update_obj)

    # Assert
    assert res.id == group_mission.id
    assert res.group_id == group.id
    assert res.status == arrange_status
    if arrange_status in date_close_status_list:
        assert isinstance(res.date_close, datetime)


# pytest tests/tmain/repository/test_mission.py::test_group_mission_update_entity_not_found_error -v -s
@pytest.mark.asyncio
async def test_group_mission_update_entity_not_found_error(dl: dataloader, repo_mission: IRepositoryMission):
    # Arrange
    group = await dl.group_loader.create()
    group_mission_not_exist_id = -1

    update_obj = MissionGroupUpdateDTO(status=OccupancyStatusEnum.FINISH)

    # Act
    with pytest.raises(EntityNotFound) as e:
        await repo_mission.group_mission_update(id=group_mission_not_exist_id, group_id=group.id, obj=update_obj)
    # Assert
    assert f"id={group_mission_not_exist_id}" in str(e.value)


async def _arrange_group_mission_list_filter_group_id(dl: dataloader) -> tuple[set[int], MissionGroupFilter]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()
    group_fictitious = await dl.group_loader.create()

    group_mission_1 = await dl.create_group_mission(user=user, group=group)
    group_mission_2 = await dl.create_group_mission(user=user, group=group)
    group_mission_3 = await dl.create_group_mission(user=user, group=group)
    await dl.create_group_mission(user=user, group=group_fictitious)
    await dl.create_group_mission(user=user, group=group_fictitious)

    filter_obj = MissionGroupFilter(group_id=group.id)
    filtered_objects_set_id = {group_mission_1.id, group_mission_2.id, group_mission_3.id}
    return filtered_objects_set_id, filter_obj


async def _arrange_group_mission_list_filter_group_id_list(dl: dataloader) -> tuple[set[int], MissionGroupFilter]:
    user = await dl.user_loader.create()
    group_1 = await dl.group_loader.create()
    group_2 = await dl.group_loader.create()
    group_3 = await dl.group_loader.create()
    group_fictitious = await dl.group_loader.create()

    group_mission_1 = await dl.create_group_mission(user=user, group=group_1)
    group_mission_2 = await dl.create_group_mission(user=user, group=group_2)
    group_mission_3 = await dl.create_group_mission(user=user, group=group_3)
    await dl.create_group_mission(user=user, group=group_fictitious)
    await dl.create_group_mission(user=user, group=group_fictitious)

    filter_obj = MissionGroupFilter(group_id_list=[group_1.id, group_2.id, group_3.id])
    filtered_objects_set_id = {group_mission_1.id, group_mission_2.id, group_mission_3.id}
    return filtered_objects_set_id, filter_obj


async def _arrange_group_mission_list_filter_mission_id(dl: dataloader) -> tuple[set[int], MissionGroupFilter]:
    user = await dl.user_loader.create()
    mission = await dl.create_mission()
    group = await dl.group_loader.create()
    group_fictitious = await dl.group_loader.create()

    group_mission_1 = await dl.create_group_mission(user=user, group=group, mission=mission)
    group_mission_2 = await dl.create_group_mission(user=user, group=group, mission=mission)
    group_mission_3 = await dl.create_group_mission(user=user, group=group, mission=mission)
    await dl.create_group_mission(user=user, group=group_fictitious)
    await dl.create_group_mission(user=user, group=group_fictitious)

    filter_obj = MissionGroupFilter(mission_id=mission.id)
    filtered_objects_set_id = {group_mission_1.id, group_mission_2.id, group_mission_3.id}
    return filtered_objects_set_id, filter_obj


async def _arrange_group_mission_list_filter_status(dl: dataloader) -> tuple[set[int], MissionGroupFilter]:
    user = await dl.user_loader.create()
    group = await dl.group_loader.create()

    group_mission_1 = await dl.create_group_mission(user=user, group=group, status=OccupancyStatusEnum.ACTIVE)
    group_mission_2 = await dl.create_group_mission(user=user, group=group, status=OccupancyStatusEnum.ACTIVE)
    await dl.create_group_mission(user=user, group=group, status=OccupancyStatusEnum.FINISH)
    await dl.create_group_mission(user=user, group=group, status=OccupancyStatusEnum.REJECT)
    await dl.create_group_mission(user=user, group=group, status=OccupancyStatusEnum.FINISH)

    filter_obj = MissionGroupFilter(status=OccupancyStatusEnum.ACTIVE)
    filtered_objects_set_id = {group_mission_1.id, group_mission_2.id}
    return filtered_objects_set_id, filter_obj


# pytest tests/tmain/repository/test_mission.py::test_group_mission_list_filter -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _arrange_group_mission_list_filter_status,
        _arrange_group_mission_list_filter_mission_id,
        _arrange_group_mission_list_filter_group_id_list,
        _arrange_group_mission_list_filter_group_id,
    ],
)
async def test_group_mission_list_filter(dl: dataloader, repo_mission: IRepositoryMission, arrange_func):
    # Arrange
    arrange_group_mission_set_id, arrange_filter_obj = await arrange_func(dl=dl)

    # Act
    res = await repo_mission.group_mission_lst(
        filter_obj=arrange_filter_obj, sorting_obj=SortGroupMissionObj(), iterable_obj=IterableObj()
    )

    res_group_mission_set_id = {group_mission.id for group_mission in res.items}

    # Assert
    assert arrange_group_mission_set_id == res_group_mission_set_id


async def _arrange_group_mission_pagination_list_offset_0_limit_none(
    dl: dataloader,
) -> tuple[int, int, int, int | None]:
    await dl.create_group_mission_list_random(count=20)
    return 20, 20, 0, None


async def _arrange_group_mission_pagination_list_offset_19_limit_none(
    dl: dataloader,
) -> tuple[int, int, int, int | None]:
    await dl.create_group_mission_list_random(count=20)
    return 20, 1, 19, None


async def _arrange_group_mission_pagination_list_offset_0_limit_17(
    dl: dataloader,
) -> tuple[int, int, int, int | None]:
    await dl.create_group_mission_list_random(count=20)
    return 20, 17, 0, 17


async def _arrange_group_mission_pagination_list_offset_17_limit_6(
    dl: dataloader,
) -> tuple[int, int, int, int | None]:
    await dl.create_group_mission_list_random(count=20)
    return 20, 3, 17, 6


# pytest tests/tmain/repository/test_mission.py::test_group_mission_pagination -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _arrange_group_mission_pagination_list_offset_0_limit_none,
        _arrange_group_mission_pagination_list_offset_19_limit_none,
        _arrange_group_mission_pagination_list_offset_0_limit_17,
        _arrange_group_mission_pagination_list_offset_17_limit_6,
    ],
)
async def test_group_mission_pagination(dl: dataloader, repo_mission: IRepositoryMission, arrange_func):
    # Arrange
    total, arrange_count, arrange_offset, arrange_limit = await arrange_func(dl=dl)

    # Act
    res = await repo_mission.group_mission_lst(
        filter_obj=MissionGroupFilter(),
        sorting_obj=SortGroupMissionObj(),
        iterable_obj=IterableObj(limit=arrange_limit, offset=arrange_offset),
    )

    # Assert
    assert res.limit == arrange_limit
    assert res.offset == arrange_offset
    assert res.total == total
    assert len(res.items) == arrange_count
