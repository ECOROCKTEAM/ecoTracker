from dataclasses import dataclass
from src.core.dto.community.privacy import PrivacyDTO
from src.core.entity.user import User

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.community import IRepositoryCommunity


@dataclass
class Result:
    item: list[PrivacyDTO]


class CommunityPrivacyListUsecase:
    def __init__(self, *, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        privacy_list = await self.repo.privacy_list()
        return Result(item=privacy_list)
