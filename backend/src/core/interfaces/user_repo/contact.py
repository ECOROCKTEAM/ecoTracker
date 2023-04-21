from abc import abstractmethod, ABC

class iContactRepository(ABC):
    @abstractmethod
    async def user_contact_create(self, *, obj: UserContactCreateDTO) -> UserContactDTO:
        """Contact creating by user for himself

        Args:
            obj (UserContactCreateDTO): DTO for create user contact object

        Returns:
            UserContactDTO: DTO of user contact object
        """

    @abstractmethod
    async def user_contact_update(self, *, user_contact: UserContactDTO, obj: UserContactUpdateDTO) -> UserContactDTO:
        """updating user contact

        Args:
            user_contact (UserContactDTO): DTO of user contact object
            obj (UserContactUpdateDTO): DTO for update user contact object

        Returns:
            UserContactDTO: DTO of user contact object
        """

    @abstractmethod # возможно в нашей m2m модели будет поле id и в таком случае будет проще искать... наверное
    async def user_contact_delete(self, *, obj: UserContactDeleteDTO) -> int:
        """delete contact from user contact list

        Args:
            obj (UserContactDeleteDTO): DTO for delete user contact object

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
                           ) -> list[UserContactDTO]:
        """User contact list

        Args:
            user_id (str): user identify
            filter_obj (MockObj): Some filter item
            sorting_obj (MockObj): Some sorting obj
            order_obj (MockObj): Some order obj

        Returns:
            list[UserContactDTO]: list of DTO user contact objects
        """
        pass

    @abstractmethod
    async def user_contact_get(self, *, obj: UserContactGetDTO) -> UserContactDTO:
        """get one contact

        Args:
            obj (UserContactGetDTO): DTO for get one user contact object

        Returns:
            UserContactDTO: DTO of user contact object
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
