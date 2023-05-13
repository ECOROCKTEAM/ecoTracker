from dataclasses import dataclass

from src.core.dto.community.community import CommunityCreateDTO
from src.core.dto.m2m.user.community import UserCommunityCreateDTO
from src.core.entity.community import Community
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: Community


class CommunityCreateUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, create_obj: CommunityCreateDTO) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            community = await self.uow.community.create(obj=create_obj)
            await self.uow.community.user_add(
                obj=UserCommunityCreateDTO(user_id=user.id, community_id=community.id, role=CommunityRoleEnum.SUPERUSER)
            )
            await uow.commit()
        return Result(item=community)
