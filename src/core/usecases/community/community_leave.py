from dataclasses import dataclass

from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.community import CommunityLeaveError
from src.core.interfaces.repository.community.community import CommunityUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: bool


class CommunityLeaveUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, user: User, community_id: int) -> Result:
        async with self.uow as uow:
            role = await uow.community.user_get(community_id=community_id, user_id=user.id)
            if role.role == CommunityRoleEnum.SUPERUSER:
                superuser_list = await uow.community.user_list(
                    id=community_id, filter_obj=CommunityUserFilter(role_list=[CommunityRoleEnum.SUPERUSER])
                )
                if len(superuser_list) == 1:
                    raise CommunityLeaveError(user_id=user.id, community_id=community_id)
            res = await uow.community.user_remove(community_id=community_id, user_id=user.id)
            await uow.commit()
        return Result(item=res)
