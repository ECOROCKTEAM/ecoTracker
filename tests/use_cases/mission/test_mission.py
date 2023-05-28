from typing import Tuple

import pytest

from src.core.dto.challenges.mission import (
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.entity.mission import Mission, MissionCommunity, MissionUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotActive
from src.core.interfaces.repository.challenges.mission import (
    MissionCommunityFilter,
    MissionFilter,
    MissionUserFilter,
)
from src.core.usecases.challenges.mission import (
    mission_community_create,
    mission_community_get,
    mission_community_list,
    mission_community_update,
    mission_get,
    mission_list,
    mission_user_create,
    mission_user_get,
    mission_user_list,
    mission_user_update,
)
from src.data.models.challenges.mission import MissionModel
from src.data.unit_of_work import SqlAlchemyUnitOfWork


# python -m pytest tests/use_cases/mission/test_mission.py::test_list -v -s
@pytest.mark.asyncio
async def test_list(pool, test_get_mission_list_ok: Tuple[User, Mission, Mission]):
    user, test_mission_active, test_mission_not_active = test_get_mission_list_ok
    uow = SqlAlchemyUnitOfWork(pool)
    uc = mission_list.MissionListUsecase(uow=uow)

    # Default args
    default_kw = dict(order_obj=MockObj(), pagination_obj=MockObj())

    # Filter empty
    filter_obj = MissionFilter()
    res = await uc(user=user, filter_obj=filter_obj, **default_kw)
    result = res.item
    assert len(result) == 1
    mission = result[0]
    assert mission.id == test_mission_active.id
    assert mission.id != test_mission_not_active.id
    assert mission.language == user.language


# python -m pytest tests/use_cases/mission/test_mission.py::test_get -v -s
@pytest.mark.asyncio
async def test_get(pool, test_get_mission_ok: Tuple[User, Mission]):
    user, test_mission = test_get_mission_ok
    uow = SqlAlchemyUnitOfWork(pool)
    uc = mission_get.MissionGetUsecase(uow=uow)
    res = await uc(user=user, id=test_mission.id)
    mission = res.item
    assert test_mission.id == mission.id
    assert test_mission.active == mission.active
    assert mission.active == True
    assert test_mission.score == mission.score
    assert test_mission.description == mission.description
    assert test_mission.instruction == mission.instruction
    assert test_mission.category_id == mission.category_id
    assert test_mission.language == mission.language


# python -m pytest tests/use_cases/mission/test_mission.py::test_get_not_active -v -s
@pytest.mark.asyncio
async def test_get_not_active(pool, test_get_mission_not_active: Tuple[User, Mission]):
    user, test_mission = test_get_mission_not_active
    uow = SqlAlchemyUnitOfWork(pool)
    uc = mission_get.MissionGetUsecase(uow=uow)
    with pytest.raises(EntityNotActive):
        _ = await uc(user=user, id=test_mission.id)


# # python -m pytest tests/use_cases/test_mission.py::test_mission_community_get -v -s
# @pytest.mark.asyncio
# async def test_mission_community_get(
#     pool, test_user: User, test_user_community, test_community_mission: MissionCommunity
# ):
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = mission_community_get.MissionCommunityGetUsecase(uow=uow)
#     res = await uc(
#         user=test_user, mission_id=test_community_mission.mission_id, community_id=test_community_mission.community_id
#     )
#     mission = res.item
#     assert mission.community_id == test_community_mission.community_id
#     assert mission.mission_id == test_community_mission.mission_id
#     assert mission.author == test_community_mission.author
#     assert mission.status == test_community_mission.status
#     assert mission.place == test_community_mission.place
#     assert mission.meeting_date == test_community_mission.meeting_date
#     assert mission.people_required == test_community_mission.people_required
#     assert mission.people_max == test_community_mission.people_max
#     assert mission.comment == test_community_mission.comment


# # python -m pytest tests/use_cases/test_mission.py::test_mission_community_create -v -s
# @pytest.mark.asyncio
# async def test_mission_community_create(
#     pool, test_user_2: User, test_community_2: Community, test_user_community_2, test_mission: Mission
# ):
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = mission_community_create.MissionCommunityCreateUsecase(uow=uow)
#     res = await uc(
#         user=test_user_2,
#         create_obj=MissionCommunityCreateDTO(
#             community_id=test_community_2.id,
#             mission_id=test_mission.id,
#             author=test_user_2.username,
#         ),
#     )
#     mission = res.item
#     assert mission.mission_id == test_mission.id
#     assert mission.community_id == test_community_2.id
#     assert mission.author == test_user_2.username
#     assert mission.status == OccupancyStatusEnum.ACTIVE


# # python -m pytest tests/use_cases/test_mission.py::test_mission_community_update -v -s
# @pytest.mark.asyncio
# async def test_mission_community_update(
#     pool, test_user: User, test_user_community, test_community_mission: MissionCommunity
# ):
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = mission_community_update.MissionCommunityUpdateUsecase(uow=uow)
#     res = await uc(
#         user=test_user,
#         mission_id=test_community_mission.mission_id,
#         community_id=test_community_mission.community_id,
#         update_obj=MissionCommunityUpdateDTO(status=OccupancyStatusEnum.FINISH),
#     )
#     mission = res.item
#     assert mission.mission_id == test_community_mission.mission_id
#     assert mission.community_id == test_community_mission.community_id
#     assert mission.status == OccupancyStatusEnum.FINISH


# # python -m pytest tests/use_cases/test_mission.py::test_mission_community_list -v -s
# @pytest.mark.asyncio
# async def test_mission_community_list(
#     pool, test_user: User, test_user_community: UserCommunityDTO, test_community_mission: MissionCommunity
# ):
#     print()
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = mission_community_list.MissionCommunityListUsecase(uow=uow)
#     res = await uc(user=test_user, filter_obj=MissionCommunityFilter(), order_obj=MockObj(), pagination_obj=MockObj())
#     mission_list = res.item
#     print(mission_list)
#     assert len(mission_list) != 0
#     mission = mission_list[0]
#     print(mission)
#     assert mission.community_id == test_user_community.community_id
#     assert mission.mission_id == test_community_mission.community_id


# # python -m pytest tests/use_cases/test_mission.py::test_mission_user_get -v -s
# @pytest.mark.asyncio
# async def test_mission_user_get(pool, test_user: User, test_user_mission: MissionUser):
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = mission_user_get.MissionUserGetUsecase(uow=uow)
#     res = await uc(user=test_user, mission_id=test_user_mission.mission_id)
#     mission = res.item
#     assert mission.user_id == test_user_mission.user_id
#     assert mission.mission_id == test_user_mission.mission_id
#     assert mission.status == test_user_mission.status


# # python -m pytest tests/use_cases/test_mission.py::test_mission_user_create -v -s
# @pytest.mark.asyncio
# async def test_mission_user_create(pool, test_user_2: User, test_mission: Mission):
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = mission_user_create.MissionUserCreateUsecase(uow=uow)
#     res = await uc(user=test_user_2, create_obj=MissionUserCreateDTO(mission_id=test_mission.id))
#     mission = res.item
#     assert mission.user_id == test_user_2.id
#     assert mission.mission_id == test_mission.id
#     assert mission.status == OccupancyStatusEnum.ACTIVE


# # python -m pytest tests/use_cases/test_mission.py::test_mission_user_update -v -s
# @pytest.mark.asyncio
# async def test_mission_user_update(pool, test_user: User, test_user_mission: MissionUser):
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = mission_user_update.MissionUserUpdateUsecase(uow=uow)
#     res = await uc(
#         user=test_user,
#         mission_id=test_user_mission.mission_id,
#         update_obj=MissionUserUpdateDTO(status=OccupancyStatusEnum.FINISH),
#     )
#     mission = res.item
#     assert mission.user_id == test_user.id
#     assert mission.mission_id == test_user_mission.mission_id
#     assert mission.status == OccupancyStatusEnum.FINISH


# # python -m pytest tests/use_cases/test_mission.py::test_mission_user_list -v -s
# @pytest.mark.asyncio
# async def test_mission_user_list(pool, test_user: User, test_user_mission_model_list):
#     uow = SqlAlchemyUnitOfWork(pool)
#     uc = mission_user_list.MissionUserListUsecase(uow=uow)
#     res = await uc(user=test_user, filter_obj=MissionUserFilter(), order_obj=MockObj(), pagination_obj=MockObj())
#     mission_list = res.item
#     mission_user_ids = [m.user_id for m in test_user_mission_model_list]
#     mission_mission_ids = [m.mission_id for m in test_user_mission_model_list]
#     assert len(test_user_mission_model_list) != 0
#     assert len(mission_list) != 0
#     for test_mission in test_user_mission_model_list:
#         assert test_mission.user_id in mission_user_ids
#         assert test_mission.mission_id in mission_mission_ids
