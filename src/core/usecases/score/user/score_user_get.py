from dataclasses import dataclass

from src.core.dto.user.score import UserScoreDTO
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.repository.score.score import IScoreRepository


@dataclass
class Result:
    item: UserScoreDTO


class ScoreUserGetUseCase:
    def __init__(self, repo: IScoreRepository):
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        score = await self.repo.user_score_get(user_id=user.id)
        return Result(item=score)
