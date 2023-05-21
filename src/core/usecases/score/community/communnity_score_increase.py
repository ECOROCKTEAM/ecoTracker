from dataclasses import dataclass

from src.core.dto.challenges.score import ScoreOperationValueDTO
from src.core.dto.community.score import (
    CommunityOperationWithScoreDTO,
    CommunityScoreDTO,
)
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import CommunityDeactivatedError
from src.core.exception.user import UserIsNotActivateError, UserPermissionError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: CommunityScoreDTO


class CommunityChangeRatingUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self,
        *,
        community: Community,
        user: User,
        obj: ScoreOperationValueDTO,
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)
        if not user.is_premium:
            raise UserPermissionError(user_id=user.id)
        if not community.active:
            raise CommunityDeactivatedError(community_id=community.id)

        async with self.uow as uow:
            user_community_role = await uow.community.user_get(
                community_id=community.id,
                user_id=user.id,
            )
            if user_community_role.role not in (CommunityRoleEnum.SUPERUSER, CommunityRoleEnum.ADMIN):
                raise UserPermissionError(user_id=user.id)

            action_with_rating = await uow.score_community.change(
                obj=CommunityOperationWithScoreDTO(community_id=community.id, value=obj.value, operation=obj.operation)
            )
            await uow.commit()

        return Result(item=action_with_rating)
