from abc import ABC, abstractmethod

from src.core.dto.auth.firebase import UserIdentity


class IAuthProviderRepository(ABC):
    @abstractmethod
    async def get_user_by_token(self, token: str, check_revoked: bool = True) -> UserIdentity:
        ...
