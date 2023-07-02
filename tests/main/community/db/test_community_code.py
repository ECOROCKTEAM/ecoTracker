from datetime import datetime, timedelta

import pytest

from src.core.dto.community.invite import CommunityInviteDTO, CommunityInviteUpdateDTO
from src.core.entity.community import Community
from src.core.exception.base import EntityNotFound
from src.data.repository.community import IRepositoryCommunity
from tests.fixtures.community.db.entity import (
    fxe_community_default,
    fxe_community_invite_code,
    fxe_community_invite_code_expired,
)
from tests.fixtures.community.db.model import (
    fxm_community_default,
    fxm_community_with_code,
    fxm_community_with_code_expired,
)


# pytest tests/main/community/db/test_community_code.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryCommunity, fxe_community_invite_code: CommunityInviteDTO):
    code = await repo.code_get(id=fxe_community_invite_code.community_id)
    assert fxe_community_invite_code.community_id == code.community_id
    assert fxe_community_invite_code.code == code.code
    assert fxe_community_invite_code.expire_time == code.expire_time


# pytest tests/main/community/db/test_community_code.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(repo: IRepositoryCommunity):
    with pytest.raises(EntityNotFound):
        await repo.code_get(id=1)


# pytest tests/main/community/db/test_community_code.py::test_set_ok -v -s
@pytest.mark.asyncio
async def test_set_ok(repo: IRepositoryCommunity, fxe_community_default: Community):
    exp_time = datetime.now() + timedelta(days=7)
    code = await repo.code_set(
        id=fxe_community_default.id, obj=CommunityInviteUpdateDTO(code="777", expire_time=exp_time)
    )
    assert code.community_id == fxe_community_default.id
    assert code.code == "777"
    assert code.expire_time == exp_time


# pytest tests/main/community/db/test_community_code.py::test_set_not_found -v -s
@pytest.mark.asyncio
async def test_set_not_found(repo: IRepositoryCommunity):
    with pytest.raises(EntityNotFound):
        await repo.code_set(
            id=1, obj=CommunityInviteUpdateDTO(code="777", expire_time=datetime.now() + timedelta(days=7))
        )


# pytest tests/main/community/db/test_community_code.py::test_get_by_code_ok -v -s
@pytest.mark.asyncio
async def test_get_by_code_ok(repo: IRepositoryCommunity, fxe_community_invite_code: CommunityInviteDTO):
    assert isinstance(fxe_community_invite_code.code, str)
    community_code = await repo.get_by_code(code=fxe_community_invite_code.code)
    community_get = await repo.get(id=fxe_community_invite_code.community_id)
    assert community_code.id == community_get.id


# pytest tests/main/community/db/test_community_code.py::test_get_by_code_expire_fail -v -s
@pytest.mark.asyncio
async def test_get_by_code_expire_fail(
    repo: IRepositoryCommunity, fxe_community_invite_code_expired: CommunityInviteDTO
):
    assert isinstance(fxe_community_invite_code_expired.code, str)
    with pytest.raises(EntityNotFound):
        await repo.get_by_code(code=fxe_community_invite_code_expired.code)
