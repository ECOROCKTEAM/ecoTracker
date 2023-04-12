import asyncio
from dataclasses import dataclass

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.core import IRepositoryCore
from src.core.entity.community import Community, CommunityCreateDTO


@dataclass
class Result:
    item: Community


class CommunityCreateUsecase:

    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user_id: str, create_obj: CommunityCreateDTO) -> Result:
        user_task = asyncio.create_task(self.repo.user_get(id=user_id))
        user = await user_task
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user_id)
        community = await self.repo.community_create(obj=create_obj)
        return Result(item=community)
