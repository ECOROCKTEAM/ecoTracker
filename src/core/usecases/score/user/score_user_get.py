from dataclasses import dataclass

from src.core.dto.user.score import UserScoreDTO
from src.core.interfaces.repository.score.score import IScoreRepository
from src.core.exception.user import UserIsNotActivateError
from src.core.entity.user import User


@dataclass
class Result:
    item: UserScoreDTO


class ScoreUserGetUseCase:
    def __init__(self, repo: IScoreRepository):
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)

        score = await self.repo.user_score_get(user_id=user.username)
        return Result(item=score)
