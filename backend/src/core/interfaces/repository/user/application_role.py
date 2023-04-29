from abc import ABC, abstractmethod
from typing import List

from src.core.dto.user.role import UserRoleCreateDTO, UserRoleDTO


class IApplicationRoleRepository(ABC):

    @abstractmethod
    async def list(self) -> List[UserRoleDTO]:
        """List of application role 

        Returns:
            list[UserRoleDTO]: DTO of application role objects
        """

    @abstractmethod
    async def create(self, *, obj: UserRoleCreateDTO) -> UserRoleDTO:
        """ Creating application role

        Args:
            name (str): str application name    

        Returns:
            str: str application name 
        """