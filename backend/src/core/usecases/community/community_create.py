from dataclasses import dataclass
from src.core.dto.shared import UserCommunityCreateDTO
from src.core.entity.user import User
from src.core.enum.role import CommunityRoleEnum

from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.repository.core import IRepositoryCore
from src.core.entity.community import Community, CommunityCreateDTO


@dataclass
class Result:
    item: Community


class CommunityCreateUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: CommunityCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(username=user.username)
        community = await self.repo.community_create(obj=create_obj)
        await self.repo.community_add_user(
            obj=UserCommunityCreateDTO(
                user_id=user.username,
                community_id=community.name,
                role=CommunityRoleEnum.SUPERUSER,
            )
        )
        return Result(item=community)
