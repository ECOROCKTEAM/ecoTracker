from dataclasses import dataclass

from src.core.dto.user.score import UserScoreDTO
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserScoreDTO


class UserGetScoreUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        async with self.uow as uow:
            score = await uow.score_user.user_get(user_id=user.id)

            if score.value < 0:
                score.value = 0

        return Result(item=score)
