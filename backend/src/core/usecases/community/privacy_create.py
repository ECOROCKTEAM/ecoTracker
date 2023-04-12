import asyncio
from dataclasses import dataclass
from src.core.dto.privacy import PrivacyCreateDTO, PrivacyDTO

from src.core.exception.user import UserPermissionError
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: PrivacyDTO


class CommunityPrivacyCreateUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user_id: str, create_obj: PrivacyCreateDTO) -> Result:
        user = await self.repo.user_get(id=user_id)
        if not user.application_role.ADMIN:
            raise UserPermissionError(user_id=user_id)
        privacy = await self.repo.community_privacy_create(obj=create_obj)
        return Result(item=privacy)
