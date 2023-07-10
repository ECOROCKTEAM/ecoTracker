import pytest

from src.core.dto.community.community import CommunityCreateDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.community.community_create import CommunityCreateUsecase
from tests.fixtures.community.usecase.community import mock_community_create
from tests.fixtures.community.usecase.user import mock_community_user_add_superuser
from tests.fixtures.user.usecase.entity import fxe_user_default


# pytest tests/main/community/usecases/community/test_create.py::test_ok -v -s
@pytest.mark.asyncio
async def test_ok(
    uow: IUnitOfWork,
    fxe_user_default: User,
    mock_community_create: Community,
    mock_community_user_add_superuser: UserCommunityDTO,
):
    uc = CommunityCreateUsecase(uow=uow)
    res = await uc(
        user=fxe_user_default,
        create_obj=CommunityCreateDTO(
            name=mock_community_create.name,
            privacy=mock_community_create.privacy,
            description=mock_community_create.description,
            active=mock_community_create.active,
        ),
    )
    community = res.item
    assert community.id == mock_community_create.id
    assert community.name == mock_community_create.name
    assert community.description == mock_community_create.description
    assert community.active == mock_community_create.active
    assert community.privacy == mock_community_create.privacy
