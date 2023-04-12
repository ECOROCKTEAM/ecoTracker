import asyncio
from dataclasses import dataclass
from typing import Tuple

from src.core.dto.shared import UserCommunityCreateDTO, UserCommunityDTO
from src.core.entity.user import User
from src.core.exception.community import CommunityPrivacyError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.core import IRepositoryCore
from src.core.entity.community import Community


@dataclass
class Result:
    item: UserCommunityDTO


class UserCommunityPublicCreateUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, create_obj: UserCommunityCreateDTO) -> Result:
        user_id = create_obj.user_id
        community_id = create_obj.community_id

        tasks: Tuple[asyncio.Task[User], asyncio.Task[Community]] = (
            asyncio.create_task(self.repo.user_get(id=user_id)),
            asyncio.create_task(self.repo.community_get(id=community_id)),
        )
        user, community = await asyncio.gather(*tasks)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user_id)
        if not community.privacy.PUBLICK:
            raise CommunityPrivacyError(community_id=community_id)
        link = await self.repo.community_add_user(obj=create_obj)
        return Result(item=link)
