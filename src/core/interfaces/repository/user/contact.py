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
    async def get_favorite(self, *, user_id: str) -> ContactUserDTO:
        """Get user favorite contact

        Args:
            user_id (str): user identify

        Returns:
            ContactUserDTO: User contact object DTO
        """

    @abstractmethod
    async def delete(self, *, id: int) -> int:
        """Delete user contact

        Args:
            id (int): User contact identify

        Returns:
            int: Deleted user contact identify
        """

    @abstractmethod
    async def get(self, *, id: int) -> ContactUserDTO:
        """Get user contact object

        Args:
            id (int): User contact identify

        Returns:
            ContactUserDTO: User contact object DTO
        """

    @abstractmethod
    async def set_favorite(self, *, id: int, is_favorite: bool) -> ContactUserDTO:
        """Set contact as favorite

        Args:
            id (int): User contact identify
            is_favorite (bool): Set as favorite/unfavorite to user contact value

        Returns:
            ContactUserDTO: ContactUserDTO entity
        """

    @abstractmethod
    async def create(self, *, user_id: str, obj: ContactUserCreateDTO) -> ContactUserDTO:
        """Create user contact

        Args:
            user_id (str): user identify
            obj (ContactUserCreateDTO): DTO for create user contact object

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def update(self, *, obj: ContactUserUpdateDTO) -> ContactUserDTO:
        """Update user contact

        Args:
            obj (ContactUserUpdateDTO): DTO for update

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def list(
        self,
        *,
        user_id: str,
        filter_obj: UserContactFilter,
        sorting_obj: UserContactSorting,
        order_obj: UserContactOrder,
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
