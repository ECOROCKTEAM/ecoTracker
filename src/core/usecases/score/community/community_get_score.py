from dataclasses import dataclass

from src.core.dto.community.score import CommunityScoreDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.exception.community import CommunityDeactivatedError
from src.core.exception.user import UserIsNotActivateError, UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: CommunityScoreDTO


class CommunityGetScoreUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        community: Community,
        user: User,
    ) -> Result:
        if not community.active:
            raise CommunityDeactivatedError(community_id=community.id)
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            community_score = await uow.score_community.community_get(community_id=community.id)

            if community_score.value < 0:
                community_score.value = 0

        return Result(item=community_score)
