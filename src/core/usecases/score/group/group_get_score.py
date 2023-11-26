from dataclasses import dataclass

from src.core.dto.group.score import GroupScoreDTO
from src.core.entity.user import User
from src.core.exception.group import GroupDeactivatedError
from src.core.exception.user import UserIsNotActivateError, UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: GroupScoreDTO


class GroupGetScoreUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        group_id: int,
        user: User,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            group = await uow.group.get(id=group_id)
            if not group.active:
                raise GroupDeactivatedError(group_id=group.id)

            group_score = await uow.score_group.group_get(group_id=group.id)

            if group_score.value < 0:
                group_score.value = 0

        return Result(item=group_score)
