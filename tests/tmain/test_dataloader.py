import pytest

from src.core.enum.group.role import GroupRoleEnum
from tests.dataloader import dataloader


# pytest tests/tmain/test_dataloader.py::test_tracking -v -s
@pytest.mark.asyncio
async def test_tracking(dl: dataloader):
    print()
    u = await dl.user_loader.create()
    u2 = await dl.user_loader.create()

    g = await dl.group_loader.create()
    g1 = await dl.group_loader.create()
    g2 = await dl.group_loader.create()

    await dl.user_group_loader.create(user=u, group=g, role=GroupRoleEnum.ADMIN)
    await dl.user_group_loader.create(user=u, group=g1, role=GroupRoleEnum.ADMIN)
    await dl.user_group_loader.create(user=u, group=g2, role=GroupRoleEnum.ADMIN)

    await dl.user_group_loader.create(user=u2, group=g, role=GroupRoleEnum.ADMIN)
    await dl.user_group_loader.create(user=u2, group=g1, role=GroupRoleEnum.ADMIN)
