from datetime import datetime, timedelta

import pytest

from src.core.dto.group.invite import GroupInviteDTO, GroupInviteUpdateDTO
from src.core.entity.group import Group
from src.core.exception.base import EntityNotFound
from src.data.repository.group import IRepositoryGroup
from tests.fixtures.group.db.entity import (
    fxe_group_default,
    fxe_group_invite_code,
    fxe_group_invite_code_expired,
)
from tests.fixtures.group.db.model import (
    fxm_group_default,
    fxm_group_with_code,
    fxm_group_with_code_expired,
)


# pytest tests/main/group/db/test_group_code.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(repo: IRepositoryGroup, fxe_group_invite_code: GroupInviteDTO):
    code = await repo.code_get(id=fxe_group_invite_code.group_id)
    assert fxe_group_invite_code.group_id == code.group_id
    assert fxe_group_invite_code.code == code.code
    assert fxe_group_invite_code.expire_time == code.expire_time


# pytest tests/main/group/db/test_group_code.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(repo: IRepositoryGroup):
    with pytest.raises(EntityNotFound):
        await repo.code_get(id=1)


# pytest tests/main/group/db/test_group_code.py::test_set_ok -v -s
@pytest.mark.asyncio
async def test_set_ok(repo: IRepositoryGroup, fxe_group_default: Group):
    exp_time = datetime.now() + timedelta(days=7)
    code = await repo.code_set(id=fxe_group_default.id, obj=GroupInviteUpdateDTO(code="777", expire_time=exp_time))
    assert code.group_id == fxe_group_default.id
    assert code.code == "777"
    assert code.expire_time == exp_time


# pytest tests/main/group/db/test_group_code.py::test_set_not_found -v -s
@pytest.mark.asyncio
async def test_set_not_found(repo: IRepositoryGroup):
    with pytest.raises(EntityNotFound):
        await repo.code_set(id=1, obj=GroupInviteUpdateDTO(code="777", expire_time=datetime.now() + timedelta(days=7)))


# pytest tests/main/group/db/test_group_code.py::test_get_by_code_ok -v -s
@pytest.mark.asyncio
async def test_get_by_code_ok(repo: IRepositoryGroup, fxe_group_invite_code: GroupInviteDTO):
    assert isinstance(fxe_group_invite_code.code, str)
    group_code = await repo.get_by_code(code=fxe_group_invite_code.code)
    group_get = await repo.get(id=fxe_group_invite_code.group_id)
    assert group_code.id == group_get.id


# pytest tests/main/group/db/test_group_code.py::test_get_by_code_expire_fail -v -s
@pytest.mark.asyncio
async def test_get_by_code_expire_fail(repo: IRepositoryGroup, fxe_group_invite_code_expired: GroupInviteDTO):
    assert isinstance(fxe_group_invite_code_expired.code, str)
    with pytest.raises(EntityNotFound):
        await repo.get_by_code(code=fxe_group_invite_code_expired.code)
