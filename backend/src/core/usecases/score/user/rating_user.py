from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.interfaces.challenges.score.score import IScoreRepository
from src.core.dto.user.score import UserBoundOffsetDTO, UserScoreDTO
from src.core.exception.user import UserIsNotPremiumError, UserIsNotActivateError
from src.core.entity.user import User


@dataclass
class Result:
    items: list[dict([(int, UserScoreDTO)])]


class RatingUserUseCase:
    def __init__(self, repo: IScoreRepository):
        self.repo = repo

    async def __call__(
        self, *,
        order_obj: MockObj, 
        bound_offset: int = None,
        user: User = None,
    ) -> Result:
        
        if not user.active:
            raise UserIsNotActivateError(
                username=user.username, deactivated=user.active
            )
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)

        if all([bound_offset, user]):
            bound = UserBoundOffsetDTO(
                username=user.username,
                bound_offset=bound_offset
            )
            score = await self.repo.rating_user(obj=bound, order_obj=order_obj)

        score = await self.repo.rating_user(order_obj)

        return Result(items=score)
