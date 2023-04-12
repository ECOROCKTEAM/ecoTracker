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
        user = await self.repo.user_get(id=user_id)
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user_id)
        community = await self.repo.community_create(obj=create_obj)
        # TODO LINK WITH USER
        return Result(item=community)
