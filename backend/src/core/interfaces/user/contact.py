from abc import abstractmethod, ABC

from src.core.dto.mock import MockObj
from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.dto.user.contact import ContactTypeCreateDTO, ContactTypeDTO
from src.core.dto.m2m.user.contact import ContactUserCreateDTO, ContactUserUpdateDTO


class IUserContactRepository(ABC):

    @abstractmethod
    async def user_contact_create(self, *, obj: ContactUserCreateDTO) -> ContactUserDTO:
        """Contact creating by user for himself

        Args:
            obj (ContactUserCreateDTO): DTO for create user contact object

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def user_contact_update(self, *, obj: ContactUserUpdateDTO) -> ContactUserDTO:
        """Updating user contact

        Args:
            obj (ContactUserUpdateDTO): DTO for update user contact object

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def user_contact_delete(self, *, contact_id: int) -> int:
        """Delete contact from user contact list

        Args:
            contact_id: int of user contact object

        Returns:
            int: id of deleted contact
        """
    pass

    @abstractmethod
    async def user_contact_list(
        self, *, 
        user_id: str, 
        filter_obj: MockObj, 
        sorting_obj: MockObj, 
        order_obj: MockObj
                           ) -> list[ContactUserDTO]:
        """User contact list

        Args:
            user_id (str): user identify
            filter_obj (MockObj): Some filter item
            sorting_obj (MockObj): Some sorting obj
            order_obj (MockObj): Some order obj

        Returns:
            list[ContactUserDTO]: List of DTO user contact objects
        """
        pass

    @abstractmethod
    async def user_contact_get(self, *, id: int) -> ContactUserDTO:
        """Get one contact

        Args:
            id (int): int of user contact object

        Returns:
            ContactUserDTO: DTO of user contact object
        """

    @abstractmethod
    async def contact_type_create(self, *, obj: ContactTypeCreateDTO) -> ContactTypeDTO:
        """ Creating contact type

        Args:
            obj (ContactTypeCreateDTO): DTO for create contact type

        Returns:
            ContactTypeDTO: DTO of contact type object
        """
        pass
