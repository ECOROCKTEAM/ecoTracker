import pytest

from src.core.entity.occupancy import OccupancyCategory
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.occupancy.occupancy_get import (
    OccupancyCategoryGetUsecase,
)
from tests.fixtures.challenges.category.usecase.category import (
    mock_category_get_default,
)
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/challenges/occupancy_category/usecases/test_get.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_category_get_default: OccupancyCategory,
):
    uc = OccupancyCategoryGetUsecase(uow=uow)
    res = await uc(user=fxe_user_default, id=1)
    oc = res.item
    assert isinstance(oc, OccupancyCategory)
    assert mock_category_get_default.id == oc.id
