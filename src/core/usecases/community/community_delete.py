from dataclasses import dataclass

from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.user import UserIsNotCommunitySuperUserError, UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: int


class CommunityDeleteUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, community_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            user_role = await uow.community.user_get(community_id=community_id, user_id=user.id)
            # raised EntityNotFound if user is not member
            if user_role.role != CommunityRoleEnum.SUPERUSER:
                raise UserIsNotCommunitySuperUserError(username=user.username, community_id=community_id)

            deactivate_id = await uow.community.deactivate(id=community_id)
            await uow.commit()
            return Result(item=deactivate_id)
