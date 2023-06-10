import pytest

from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.interfaces.repository.challenges.mission import MissionCommunityFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission.mission_community_list import (
    MissionCommunityListUsecase,
)
from tests.fixtures.community.usecase.community import mock_community_lst
from tests.fixtures.user.usecase.entity import fxe_user_default


# python -m pytest tests/challenges/mission/usecases/community_mission/test_community_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_lst,
):
    uc = MissionCommunityListUsecase(uow=uow)
    await uc(
        user=fxe_user_default,
        filter_obj=MissionCommunityFilter(),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
