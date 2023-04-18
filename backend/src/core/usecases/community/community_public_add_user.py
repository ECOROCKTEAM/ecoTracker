from dataclasses import dataclass

from src.core.dto.m2m.user_community import UserCommunityCreateDTO, UserCommunityDTO
from src.core.entity.user import User
from src.core.exception.community import (
    CommunityDeactivatedError,
    CommunityPrivacyError,
)
from src.core.exception.user import UserIsNotPremiumError, UserPermissionError
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: UserCommunityDTO


class CommunityPublicAddUserUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(
        self, *, user: User, create_obj: UserCommunityCreateDTO
    ) -> Result:
        if user.username != create_obj.user_id:
            raise UserPermissionError(username=user.username)
        community_id = create_obj.community_id
        community = await self.repo.community_get(id=community_id)
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        if not community.active:
            raise CommunityDeactivatedError(community_id=community_id)
        if not community.privacy.enum.PUBLICK:
            raise CommunityPrivacyError(community_id=community_id)
        link = await self.repo.community_user_add(obj=create_obj)
        return Result(item=link)
