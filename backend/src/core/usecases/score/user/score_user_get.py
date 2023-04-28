from dataclasses import dataclass

from src.core.dto.score import ScoreUserDTO
from src.core.exception.user import UserIsNotActivateError
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User


@dataclass
class Result:
    item: ScoreUserDTO


class ScoreUserGetUseCase:
    def __init__(self, repo: IRepositoryCore):
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.active:
            raise UserIsNotActivateError(
                username=user.username, deactivated=user.active
            )

        score = await self.repo.score_user_get(username=user.username)

        return Result(item=score)
