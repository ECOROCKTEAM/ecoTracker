from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.mock import MockObj
from src.core.dto.user.score import (
    OperationWithScoreUserDTO,
    UserBoundOffsetDTO,
    UserScoreDTO,
)
from src.core.interfaces.repository.score.user import IRepositoryUserScore


class UserScoreRepository(IRepositoryUserScore):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def user_change(self, *, obj: OperationWithScoreUserDTO) -> UserScoreDTO:
        return await super().user_change(obj=obj)

    async def user_get(self, *, user_id: int) -> UserScoreDTO:
        return await super().user_get(user_id=user_id)

    async def user_rating(
        self, *, obj: UserBoundOffsetDTO | None = None, order_obj: MockObj
    ) -> dict[int, UserScoreDTO]:
        return await super().user_rating(obj=obj, order_obj=order_obj)
