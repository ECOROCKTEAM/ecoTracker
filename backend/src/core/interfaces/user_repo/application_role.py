from abc import ABC, abstractmethod


class IApplicationRoleRepository(ABC):

    @abstractmethod
    async def create(self, *, name: str) -> str:
        """ Creating application role

        Args:
            name (str): str application name    

        Returns:
            str: str application name 
        """