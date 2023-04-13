from dataclasses import dataclass

from src.core.exception.base import PermissionError
from src.core.entity.user import User
from src.core.dto.subscription import SubscriptionTypeTranslateCreateDTO, SubscriptionTypeDTO
from src.core.interfaces.base import IRepositoryCore


@dataclass
class SuccessResult:
    item: SubscriptionTypeDTO


class SubscriptionTypeCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, user: User, new_type: SubscriptionTypeTranslateCreateDTO) -> SuccessResult:

        if not user.application_role.ADMIN:
            raise PermissionError(username=user.username)

        constraint = await self.repo.subscription_type_translate_create(new_obj=new_type)

        return SuccessResult(item=constraint)