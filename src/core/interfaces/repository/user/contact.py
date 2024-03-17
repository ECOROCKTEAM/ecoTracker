from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.dto.m2m.user.contact import (
    ContactUserCreateDTO,
    ContactUserDTO,
    ContactUserUpdateDTO,
)
from src.core.dto.utils import SortObj
from src.core.enum.user.contact import ContactTypeEnum


@dataclass
class UserContactFilter:
    is_favorite: bool | None = None
    active: bool | None = None
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
    async def delete(self, *, id: int, user_id: str) -> int:
        """Delete user contact

        Args:
            id (int): User contact identify
            user_id(str): User ID

        Returns:
            int: Deleted user contact identify
        """

    @abstractmethod
    async def get(self, *, id: int, user_id: str) -> ContactUserDTO:
        """Get user contact object

        Args:
            id (int): User contact identify
            user_id(str): User ID

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
    async def update(self, *, id: int, obj: ContactUserUpdateDTO, user_id: str) -> ContactUserDTO:
        """Update user contact

        Args:
            id (int): id of user contact object
            obj (ContactUserUpdateDTO): DTO for update
            user_id(str): User ID

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def lst(
        self,
        *,
        user_id: str,
        filter_obj: UserContactFilter,
        sorting_obj: SortObj,
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
