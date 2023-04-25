from abc import ABC, abstractmethod

from src.core.entity.user import User, UserCreateDTO, UserUpdateDTO


class IUserRepository(ABC):

    @abstractmethod
    async def create(self, *, obj: UserCreateDTO) -> User:
        """Create user \ Registration

        Args:
            obj (UserCreateDTO): DTO for creating user object

        Returns:
            User: User entity

        Raises:
            RepoError: Repository error
            UserDidNotCreated: User didn't created

        """

    @abstractmethod 
    async def update(self, *, obj: UserUpdateDTO) -> User:
        """User update

        Args:
            obj (UserUpdateDTO): DTO for update user

        Returns:
            User: User entity
        """
