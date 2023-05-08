from dataclasses import dataclass

from src.core.dto.challenges.score import ScoreOperationValueDTO
from src.core.exception.score import UserOperationScoreError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.dto.user.score import UserScoreDTO, OperationWithScoreUserDTO
from src.core.exception.user import UserIsNotActivateError
from src.core.entity.user import User


@dataclass
class Result:
    item: UserScoreDTO


class UserChangeScoreUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, user: User, obj: ScoreOperationValueDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            if obj.operation.MINUS:
                """If current user value more that subtrahend value."""

                current_user_score = await uow.score.user_get(user_id=user.id)
                if current_user_score.value > obj.value:
                    raise UserOperationScoreError(operation=obj.operation, user_id=user.id)

            action_with_rating = await uow.score.user_change(
                obj=OperationWithScoreUserDTO(
                    user_id=user.id,
                    value=obj.value,
                    operation=obj.operation,
                )
            )
            await uow.commit()

        return Result(item=action_with_rating)
