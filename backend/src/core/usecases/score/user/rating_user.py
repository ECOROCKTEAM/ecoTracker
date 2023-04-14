from dataclasses import dataclass
from typing import List

from src.core.exception.user import UserIsNotPremiumError
from src.core.dto.score import ScoreUserDTO
from src.core.exception.base import DomainError
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User


@dataclass
class Result:
    items: List[List[ScoreUserDTO], int]


class ScoreUserGetUC:

    def __init__(self, repo: IRepositoryCore):
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:

        if not user.active:
            raise DomainError(username=user.username, deactivated=user.active)
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        
        score = await self.repo.score_user_get(username=user.username)
        
        return Result(items=score)