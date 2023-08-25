import pytest

from src.core.dto.group.group import GroupCreateDTO
from src.core.dto.m2m.user.group import UserGroupDTO
from src.core.entity.group import Group
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_create import GroupCreateUsecase
from tests.fixtures.group.usecase.group import mock_group_create
from tests.fixtures.group.usecase.user import mock_group_user_add_superuser
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/group/usecases/group/test_create.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_group_create: Group,
    mock_group_user_add_superuser: UserGroupDTO,
):
    uc = GroupCreateUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        create_obj=GroupCreateDTO(
            name=mock_group_create.name,
            privacy=mock_group_create.privacy,
            description=mock_group_create.description,
            active=mock_group_create.active,
        ),
    )
    group = res.item
    assert group.id == mock_group_create.id
    assert group.name == mock_group_create.name
    assert group.description == mock_group_create.description
    assert group.active == mock_group_create.active
    assert group.privacy == mock_group_create.privacy
