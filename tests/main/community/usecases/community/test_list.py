import pytest

from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.interfaces.repository.community.community import CommunityFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_list import CommunityListUsecase
from tests.fixtures.community.usecase.community import mock_community_lst_check_filter
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/community/test_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_lst_check_filter: list[Community],
):
    uc = CommunityListUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        filter_obj=CommunityFilter(active=False, user_id=fxe_user_default.id),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    # active filter was changed to true
    community_list = res.item
    assert len(community_list) == 0
