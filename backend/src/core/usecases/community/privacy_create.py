from dataclasses import dataclass
from src.core.dto.community.privacy import PrivacyCreateDTO, PrivacyDTO
from src.core.entity.user import User

from src.core.exception.user import UserPermissionError
from src.core.interfaces.repository.core import IRepositoryCore


@dataclass
class Result:
    item: PrivacyDTO


class CommunityPrivacyCreateUsecase:
    def __init__(self, *, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, create_obj: PrivacyCreateDTO) -> Result:
        if not user.role.enum.ADMIN:
            raise UserPermissionError(username=user.username)
        privacy = await self.repo.community_privacy_create(obj=create_obj)
        return Result(item=privacy)
