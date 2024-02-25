from dataclasses import dataclass

from src.core.dto.user.score import UserScoreDTO
from src.core.entity.user import User
from src.core.exception.user import UserNotActive
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserScoreDTO


class UserGetScoreUsecase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserNotActive(id=user.id)

        async with self.uow as uow:
            score = await uow.score_user.get_score(user_id=user.id)

        return Result(item=score)
