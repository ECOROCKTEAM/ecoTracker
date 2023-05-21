from dataclasses import dataclass

from src.core.dto.challenges.score import ScoreOperationValueDTO
from src.core.dto.user.score import OperationWithScoreUserDTO
from src.core.entity.score import ScoreUser
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: ScoreUser


class UserChangeScoreUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, user: User, obj: ScoreOperationValueDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            action_with_rating = await uow.score_user.change(
                obj=OperationWithScoreUserDTO(
                    user_id=user.id,
                    value=obj.value,
                    operation=obj.operation,
                )
            )
            await uow.commit()

        return Result(item=action_with_rating)
