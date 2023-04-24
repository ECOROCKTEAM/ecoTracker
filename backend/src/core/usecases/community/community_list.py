from dataclasses import dataclass
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.community import IRepositoryCommunity
from src.core.dto.community.filters import CommunityListFilter
from src.core.entity.community import Community


@dataclass
class Result:
    item: list[Community]


class CommunityListUsecase:
    def __init__(self, *, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, filter_obj: CommunityListFilter) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        community_list = await self.repo.list(obj=filter_obj)
        return Result(item=community_list)
