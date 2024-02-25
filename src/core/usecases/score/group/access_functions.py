from src.core.entity.user import User
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.exception.base import EntityNotFound, PermissionError
from src.core.exception.group import GroupNotActive
from src.core.exception.user import UserNotActive, UserNotPremium
from src.core.interfaces.unit_of_work import IUnitOfWork


async def access_check_target_group(uow: IUnitOfWork, user: User, group_id: int):
    if not user.active:
        raise UserNotActive(user_id=user.id)
    if not user.is_premium:
        raise UserNotPremium(user_id=user.id)

    group = await uow.group.get(id=group_id)
    try:
        user_group = await uow.group.user_get(user_id=user.id, group_id=group_id)
    except EntityNotFound:
        user_group = None

    if group.privacy == GroupPrivacyEnum.PRIVATE and user_group is None:
        raise EntityNotFound(msg="")

    if user_group is not None and user_group.role == GroupRoleEnum.BLOCKED:
        raise PermissionError(msg=f"user_id={user.id}, {group_id=}")

    if not group.active:
        raise GroupNotActive(id=group.id)
