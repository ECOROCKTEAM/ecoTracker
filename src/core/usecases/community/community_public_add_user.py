from dataclasses import dataclass

from src.core.dto.m2m.user.community import UserCommunityCreateDTO, UserCommunityDTO
from src.core.entity.user import User
from src.core.exception.community import (
    CommunityDeactivatedError,
    CommunityPrivacyError,
)
from src.core.exception.user import UserIsNotPremiumError, UserPermissionError
from src.core.interfaces.repository.community.community import IRepositoryCommunity


@dataclass
class Result:
    item: UserCommunityDTO


class CommunityPublicAddUserUsecase:
    def __init__(self, *, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: UserCommunityCreateDTO) -> Result:
        if user.id != create_obj.user_id:
            raise UserPermissionError(user_id=user.id)
        community_id = create_obj.community_id
        community = await self.repo.get(id=community_id)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        if not community.active:
            raise CommunityDeactivatedError(community_id=community_id)
        if not community.privacy.PUBLICK:
            raise CommunityPrivacyError(community_id=community_id)
        link = await self.repo.user_add(obj=create_obj)
        return Result(item=link)
