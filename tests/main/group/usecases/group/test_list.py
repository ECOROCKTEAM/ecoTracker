import pytest

from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.interfaces.repository.group.group import GroupFilter
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_list import GroupListUsecase
from tests.fixtures.group.usecase.group import mock_group_lst_check_filter
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/group/test_list.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_lst_check_filter: list[Group],
):
    uc = GroupListUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        filter_obj=GroupFilter(active=False, user_id=fxe_user_default.id),
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    # active filter was changed to true
    group_list = res.item

    assert len(group_list) == 0
