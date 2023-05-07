from dataclasses import dataclass
from src.core.dto.m2m.user.community import UserCommunityCreateDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.community.community import IRepositoryCommunity
from src.core.entity.community import Community
from src.core.dto.community.community import CommunityCreateDTO


@dataclass
class Result:
    item: Community


class CommunityCreateUsecase:
    def __init__(self, *, repo: IRepositoryCommunity) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: CommunityCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        community = await self.repo.create(obj=create_obj)
        await self.repo.user_add(
            obj=UserCommunityCreateDTO(
                user_id=user.id,
                community_id=community.name,
                role=CommunityRoleEnum.USER,
            )
        )
        return Result(item=community)
