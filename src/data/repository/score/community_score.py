from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.community.score import (
    CommunityBoundOffsetDTO,
    CommunityOperationWithScoreDTO,
    CommunityScoreDTO,
)
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.score.community import IRepositoryCommunityScore


class CommunityScoreRepository(IRepositoryCommunityScore):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def community_change(self, *, obj: CommunityOperationWithScoreDTO) -> CommunityScoreDTO:
        return await super().community_change(obj=obj)

    async def community_get(self, *, community_id: int) -> CommunityScoreDTO:
        return await super().community_get(community_id=community_id)

    async def community_rating(
        self, *, order_obj: MockObj, obj: CommunityBoundOffsetDTO | None = None
    ) -> dict[int, CommunityScoreDTO]:
        return await super().community_rating(order_obj=order_obj, obj=obj)
