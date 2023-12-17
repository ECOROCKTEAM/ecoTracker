from abc import ABC, abstractmethod

from firebase_admin._user_mgt import UserRecord


class IFirebaseApplication(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def setup(self):
        ...

    @abstractmethod
    async def verify_token(self, token: str, check_revoked: bool = True) -> dict:
        ...

    @abstractmethod
    async def get_user(self, id: str) -> UserRecord:
        ...
