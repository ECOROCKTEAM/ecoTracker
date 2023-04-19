from dataclasses import dataclass

from src.core.exception.user import UserPermissionError
from src.core.entity.user import User
from src.core.dto.subscription import SubscriptionTypeTranslateCreateDTO, SubscriptionTypeDTO
from src.core.interfaces.base import IRepositoryCore


@dataclass
class Result:
    item: SubscriptionTypeDTO


class SubscriptionTypeCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, user: User, create_obj: SubscriptionTypeTranslateCreateDTO) -> Result:

        if not user.application_role.ADMIN:
            raise UserPermissionError(username=user.username)

        subscription_type = await self.repo.subscription_type_translate_create(obj=create_obj)

        return Result(item=subscription_type)