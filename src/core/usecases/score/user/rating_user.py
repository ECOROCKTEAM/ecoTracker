from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.dto.user.score import UserBoundOffsetDTO, UserScoreDTO
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError, UserIsNotPremiumError
from src.core.interfaces.repository.score.score import IScoreRepository


@dataclass
class Result:
    items: list[dict([(int, UserScoreDTO)])]


class RatingUserUseCase:
    def __init__(self, repo: IScoreRepository):
        self.repo = repo

    async def __call__(self, *, order_obj: MockObj, bound_offset: int | None = None, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id, deactivated=user.active)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        if all([bound_offset, user]):
            bound = UserBoundOffsetDTO(user_id=user.id, bound_offset=bound_offset)  # type: ignore
            score = await self.repo.rating_user(obj=bound, order_obj=order_obj)

        score = await self.repo.rating_user(order_obj)

        return Result(items=score)
