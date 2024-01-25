from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.dto.m2m.user.contact import (
    ContactUserCreateDTO,
    ContactUserDTO,
    ContactUserUpdateDTO,
)
from src.core.enum.user.contact import ContactTypeEnum


@dataclass
class UserContactFilter:
    is_favorite: bool | None = None
    active: bool | None = None
    type: ContactTypeEnum | None = None


@dataclass
class UserContactSorting:
    type: ContactTypeEnum | None = None
    active: bool | None = None
    is_favorite: bool | None = None


@dataclass
class UserContactOrder:
    type: ContactTypeEnum | None = None


class IUserContactRepository(ABC):
    @abstractmethod
    async def delete(self, *, contact_id: int, user_id: str) -> int:
        """Delete user contact

        Args:
            contact_id (int): Contact identify
            user_id (str): User identify

        Returns:
            int: Deleted contact identify
        """

    @abstractmethod
    async def get(self, *, user_id: str, contact_id: int) -> ContactUserDTO:
        """Get one user contact object

        Args:
            user_id (str): User identify
            contact_id (int): Contact identify

        Returns:
            ContactUserDTO: User contact object DTO
        """

    @abstractmethod
    async def set_favorite(self, *, user_id: str, contact_id: int, is_favorite: bool) -> ContactUserDTO:
        """Set contact as favorite

        Args:
            user_id (str): User identify
            contact_id (int): Contact identify
            is_favorite (bool): Set is favorite to user contact value

        Returns:
            ContactUserDTO: ContactUserDTO entity
        """

    @abstractmethod
    async def create(self, *, obj: ContactUserCreateDTO) -> ContactUserDTO:
        """Create user contact

        Args:
            obj (ContactUserCreateDTO): DTO for create user contact object

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def update(self, *, user_id: str, obj: ContactUserUpdateDTO) -> ContactUserDTO:
        """Update user contact

        Args:
            user_id (str): User identify
            obj (ContactUserUpdateDTO): DTO for update
        Args:
            contact_id: int of user contact object

        Returns:
            int: id of deleted contact
        """

    @abstractmethod
    async def list(
        self,
        *,
        user_id: str,
        filter_obj: UserContactFilter | None = None,
        sorting_obj: UserContactSorting | None = None,
        order_obj: UserContactOrder | None = None,
    ) -> list[ContactUserDTO]:
        """User contact list

        Args:
            user_id (str): user identify
            filter_obj (UserContactFilter): Filter object
            sorting_obj (UserContactSorting): Sorting object
            order_obj (UserContactGroup): Order object

        Returns:
            list[ContactUserDTO]: list of DTO user contact objects
        """
