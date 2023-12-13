from abc import ABC, abstractmethod

from src.core.dto.m2m.user.contact import (
    ContactUserCreateDTO,
    ContactUserDTO,
    ContactUserUpdateDTO,
)
from src.core.dto.mock import MockObj


class IUserContactRepository(ABC):
    @abstractmethod
    async def create(self, *, obj: ContactUserCreateDTO) -> ContactUserDTO:
        """Create user contact

        Args:
            obj (ContactUserCreateDTO): DTO for create user contact object

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def update(self, *, obj: ContactUserUpdateDTO) -> ContactUserDTO:
        """Update user contact

        Args:
            obj (ContactUserUpdateDTO): DTO for update user contact object

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def delete(self, *, contact_id: int) -> int:
        """Delete contact from user contact list

        Args:
            contact_id: int of user contact object

        Returns:
            int: id of deleted contact
        """

    pass

    @abstractmethod
    async def list(
        self,
        *,
        user_id: str,
        filter_obj: MockObj | None = None,
        sorting_obj: MockObj | None = None,
        order_obj: MockObj | None = None,
    ) -> list[ContactUserDTO]:
        """User contact list

        Args:
            user_id (str): user identify
            filter_obj (MockObj): Some filter item
            sorting_obj (MockObj): Some sorting obj
            order_obj (MockObj): Some order obj

        Returns:
            list[ContactUserDTO]: list of DTO user contact objects
        """
        pass

    @abstractmethod
    async def get(self, *, id: int) -> ContactUserDTO:
        """Get one user contact

        Args:
            id (int): int of user contact object

        Returns:
            ContactUserDTO: DTO of user contact object
        """
