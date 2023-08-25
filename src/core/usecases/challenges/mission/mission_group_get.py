from dataclasses import dataclass

from src.core.entity.mission import MissionGroup
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionGroup


class MissionGroupGetUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, id: int, group_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            user_group = await uow.group.user_get(group_id=group_id, user_id=user.id)
            if user_group.role in [GroupRoleEnum.BLOCKED]:
                raise PermissionError("")
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg="")
            group_mission = await uow.mission.group_mission_get(id=id, group_id=group_id)
        return Result(item=group_mission)
