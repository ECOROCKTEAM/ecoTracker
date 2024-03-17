from dataclasses import dataclass

from src.core.dto.statistic.group import GroupMissionCounterDTO
from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.exception.base import EntityNotActive, EntityNotFound, PermissionError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.statistic.occupancy import OccupancyStatisticFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: GroupMissionCounterDTO


class GroupMissionCounterStatisticUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, group_id: int, filter_obj: OccupancyStatisticFilter) -> Result:
        if not user.active:
            raise EntityNotActive(msg=f"{user.id=}")
        if not user.is_premium:
            raise UserIsNotPremiumError(msg=f"{user.id=}")

        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise EntityNotActive(msg=f"{group_id=}")

            try:
                await uow.group.user_get(group_id=group_id, user_id=user.id)
            except EntityNotFound:
                if group.privacy == GroupPrivacyEnum.PRIVATE:
                    raise PermissionError(msg=f"{user.id=} not in PRIVATE {group_id=}") from None

            mission_counter = await uow.group_statistic.mission_counter(group_id=group_id, filter_obj=filter_obj)
            return Result(item=mission_counter)
