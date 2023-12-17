from abc import ABC, abstractmethod

from src.core.dto.auth.firebase import UserFirebase
from src.core.interfaces.auth.firebase import IFirebaseApplication


class IAuthProviderRepository(ABC):
    @abstractmethod
    def __init__(self, firebase_app: IFirebaseApplication) -> None:
        ...

    @abstractmethod
    async def get_firebase_user_by_token(self, token: str, check_revoked: bool = True) -> UserFirebase:
        ...
