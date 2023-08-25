from dataclasses import dataclass

from src.core.dto.challenges.mission import MissionGroupCreateDTO
from src.core.entity.mission import MissionGroup
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: MissionGroup


class MissionGroupCreateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, group_id: int, create_obj: MissionGroupCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            user_group = await uow.group.user_get(group_id=group_id, user_id=user.id)
            if user_group.role not in [GroupRoleEnum.ADMIN, GroupRoleEnum.SUPERUSER]:
                raise PermissionError("")
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg=f"{group.id=}")
            mission = await uow.mission.get(id=create_obj.mission_id, lang=user.language)
            if not mission.active:
                raise EntityNotActive(msg=f"{mission.id=}")
            created_mission = await uow.mission.group_mission_create(group_id=group_id, obj=create_obj)
            await uow.commit()
        return Result(item=created_mission)
