import pytest

from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.occupancy.occupancy_get import (
    OccupancyCategoryGetUsecase,
)
from src.core.usecases.challenges.occupancy.occupancy_list import (
    OccupancyCategoryListUsecase,
)
from src.data.repository.user import model_to_dto as user_model_to_dto
from tests.dataloader import dataloader


# pytest tests/tmain/usecase/challenges/test_occupancy_category.py::test_category_get_ok -v -s
@pytest.mark.asyncio
async def test_category_get_ok(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    category = await dl.create_category()
    await dl.create_category()

    # Act
    uc = OccupancyCategoryGetUsecase(uow=uow)
    res = await uc(user=user, id=category.id)

    # Assert
    assert res.item.id == category.id


# pytest tests/tmain/usecase/challenges/test_occupancy_category.py::test_category_list_ok -v -s
@pytest.mark.asyncio
async def test_category_list_ok(dl: dataloader, uow: IUnitOfWork):
    # Arrange
    user_model = await dl.user_loader.create()
    user = user_model_to_dto(model=user_model)
    category_list = await dl.create_category_list_random()

    arrange_category_id_set = {category.id for category in category_list}

    # Act
    uc = OccupancyCategoryListUsecase(uow=uow)
    res = await uc(user=user)
    res_category_id_set = {category.id for category in res.item}

    # Assert
    assert res_category_id_set == arrange_category_id_set
