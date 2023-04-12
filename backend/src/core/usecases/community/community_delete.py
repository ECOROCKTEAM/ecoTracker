import asyncio
from typing import Tuple
from dataclasses import dataclass

from src.core.entity.user import User
from src.core.enum.role import CommunityRoleEnum
from src.core.dto.community import CommunityIncludeUserFilter
from src.core.exception.user import UserIsNotPremiumError, UserIsNotCommunitySuperUserError
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: int


class CommunityDeleteUsecase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user_id: str, community_id: str) -> Result:
        tasks: Tuple[asyncio.Task[User], asyncio.Task[list[str]]] = (
            asyncio.create_task(self.repo.user_get(id=user_id)),
            asyncio.create_task(
                self.repo.community_user_ids(
                    id=community_id, filter=CommunityIncludeUserFilter(role_list=[CommunityRoleEnum.SUPERUSER])
                )
            ),
        )
        user, super_user_ids = await asyncio.gather(*tasks)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user_id)
        if not user.id in super_user_ids:
            raise UserIsNotCommunitySuperUserError(user_id=user_id, community_id=community_id)
        rm_id = await self.repo.community_delete(id=community_id)
        return Result(item=rm_id)
