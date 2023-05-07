from dataclasses import dataclass
from src.core.dto.mock import MockObj
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.community.community import IRepositoryCommunity, CommunityFilter
from src.core.entity.community import Community


@dataclass
class Result:
    item: list[Community]


class CommunityListUsecase:
    def __init__(self, *, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(
        self, *, user: User, filter_obj: CommunityFilter, order_obj: MockObj, pagination_obj: MockObj
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        community_list = await self.repo.lst(filter_obj=filter_obj, order_obj=order_obj, pagination_obj=pagination_obj)
        return Result(item=community_list)
