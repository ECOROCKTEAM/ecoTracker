import pytest

from src.core.entity.occupancy import OccupancyCategory
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.occupancy.occupancy_list import (
    OccupancyCategoryListUsecase,
)
from tests.fixtures.challenges.category.usecase.category import (
    mock_category_lst_ret_one,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/challenges/occupancy_category/usecases/test_lst.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_category_lst_ret_one: list[OccupancyCategory],
):
    uc = OccupancyCategoryListUsecase(uow=uow)
    res = await uc(user=fxe_user_default)
    oc_list = res.item
    assert isinstance(oc_list, list)
    assert len(oc_list) == 1
    oc = oc_list[0]
    assert isinstance(oc, OccupancyCategory)
