from dataclasses import dataclass

from src.core.dto.m2m.user.community import UserCommunityCreateDTO, UserCommunityDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import (
    CommunityDeactivatedError,
    CommunityPrivacyError,
)
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserCommunityDTO


class CommunityPublicAddUserUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, community_id: int) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            community = await uow.community.get(id=community_id)
            if not community.active:
                raise CommunityDeactivatedError(community_id=community_id)
            if not community.privacy.PUBLIC:
                raise CommunityPrivacyError(community_id=community_id)
            role = await uow.community.user_add(
                obj=UserCommunityCreateDTO(user_id=user.id, community_id=community.id, role=CommunityRoleEnum.USER)
            )
            await uow.commit()
        return Result(item=role)
