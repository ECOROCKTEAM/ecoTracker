from dataclasses import dataclass

from src.core.dto.m2m.user.community import UserCommunityDTO, UserCommunityUpdateDTO
from src.core.entity.user import User
from src.core.enum.community.role import CommunityRoleEnum
from src.core.exception.base import EntityNotActive, EntityNotFound
from src.core.exception.user import PermissionError, UserIsNotPremiumError
from src.core.interfaces.repository.community.community import CommunityUserFilter
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserCommunityDTO


class CommunityChangeUserRoleUsecase:
    def __init__(self, *, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self, *, user: User, community_id: int, user_id: int, update_obj: UserCommunityUpdateDTO
    ) -> Result:
        if not user.is_premium:
            raise UserIsNotPremiumError(user_id=user.id)
        async with self.uow as uow:
            community = await uow.community.get(id=community_id)
            if not community.active:
                raise EntityNotActive(msg=f"{community.id=}")
            # that part looks like this for can be tested!
            # old realization with 2 .get methods not can be tested
            community_users = await uow.community.user_list(
                id=community.id, filter_obj=CommunityUserFilter(user_id__in=[user.id, user_id])
            )
            current_user = None
            target_user = None

            for community_user in community_users:
                if community_user.user_id == user.id:
                    current_user = community_user
                if community_user.user_id == user_id:
                    target_user = community_user

            if current_user is None:
                raise EntityNotFound(msg=f"Not found current user user_id={user.id}")
            if target_user is None:
                raise EntityNotFound(msg=f"Not found target user user_id={user_id}")
            if current_user.role not in (CommunityRoleEnum.SUPERUSER, CommunityRoleEnum.ADMIN):
                raise PermissionError(msg=f"current user is not administrator: user_id={user.id}, {community_id=}")

            if target_user.role == CommunityRoleEnum.SUPERUSER and current_user.role != CommunityRoleEnum.SUPERUSER:
                raise PermissionError(msg=f"current user is not superuser: user_id={user.id}, {community_id=}")
            link = await uow.community.user_role_update(obj=update_obj, community_id=community_id, user_id=user_id)
            await uow.commit()
        return Result(item=link)
