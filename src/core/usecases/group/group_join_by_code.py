from dataclasses import dataclass

from src.core.dto.m2m.user.group import UserGroupCreateDTO, UserGroupDTO
from src.core.entity.user import User
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotActive
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserGroupDTO


class GroupJoinByCodeUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, code: str) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            group = await uow.group.get_by_code(code)
            if not group.active:
                raise EntityNotActive(msg=f"group_id={group.id}")
            role = await uow.group.user_add(
                obj=UserGroupCreateDTO(user_id=user.id, group_id=group.id, role=GroupRoleEnum.USER)
            )
            await uow.commit()
            return Result(item=role)
