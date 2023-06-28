from dataclasses import dataclass

from src.core.dto.m2m.user.community import UserCommunityCreateDTO, UserCommunityDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import CommunityDeactivatedError
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserCommunityDTO


class CommunityJoinByCodeUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, code: str) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)

        async with self.uow as uow:
            community = await uow.community.get_by_code(code)
            if not community.active:
                raise CommunityDeactivatedError(community_id=community.id)
            role = await uow.community.user_add(
                obj=UserCommunityCreateDTO(user_id=user.id, community_id=community.id, role=CommunityRoleEnum.USER)
            )
            await uow.commit()
            return Result(item=role)
