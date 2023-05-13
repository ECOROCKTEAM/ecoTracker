from dataclasses import dataclass

from src.core.dto.community.community import CommunityUpdateDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import CommunityDeactivatedError
from src.core.exception.user import UserIsNotCommunityAdminUserError, UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: Community


class CommunityUpdateUsecase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, community_id: int, update_obj: CommunityUpdateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            community = await uow.community.get(id=community_id)
            if not community.active:
                raise CommunityDeactivatedError(community_id=community.name)
            user_role = await uow.community.user_get(community_id=community_id, user_id=user.id)
            if user_role.role not in (CommunityRoleEnum.ADMIN, CommunityRoleEnum.SUPERUSER):
                raise UserIsNotCommunityAdminUserError(user_id=user.id, community_id=community_id)

            community = await uow.community.update(id=community_id, obj=update_obj)
            await uow.commit()
        return Result(item=community)
