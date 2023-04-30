from abc import ABC, abstractmethod
from src.core.dto.mock import MockObj

from src.core.entity.mission import (
    MissionBase,
    MissionUpdateDTO,
    MissionCreateDTO,
    MissionUserCreateDTO,
    MissionUser,
    MissionUserUpdateDTO,
    MissionCommunity,
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
)


class IRepositoryMission(ABC):
    @abstractmethod
    async def get(self, *, id: int) -> MissionBase:
        """Получить базовую миссию

        Args:
            id (int): ID базовой миссии

        Returns:
            MissionBase: Сущность базовой миссии

        """

    @abstractmethod
    async def update(self, *, obj: MissionUpdateDTO) -> MissionBase:
        """Обновить базовую миссию

        Args:
            obj (MissionUpdateDTO): Объект обновления

        Returns:
            MissionBase: Сущность безовой миссии
        """

    @abstractmethod
    async def create(self, *, obj: MissionCreateDTO) -> MissionBase:
        """Создать базовую миссию

        Args:
            obj (MissionCreateDTO): Объект создания

        Returns:
            MissionBase: Сущность безовой миссии
        """

    @abstractmethod
    async def list(self, *, filter_obj: MockObj, order_obj: MockObj, pagination_obj: MockObj) -> list[MissionBase]:
        """Получить список базовых миссий

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[MissionBase]: Список базовых миссий
        """

    @abstractmethod
    async def deactivate(self, *, id: int) -> int:
        """Удалить миссию (Soft delete)

        Args:
            id (int): ID базовой миссии

        Returns:
            int: ID базовой миссии
        """

    @abstractmethod
    async def create_for_user(self, *, obj: MissionUserCreateDTO) -> MissionUser:
        """Создать миссию для пользователя

        Args:
            obj (MissionUserCreateDTO): Объект создания

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def update_for_user(self, *, obj: MissionUserUpdateDTO) -> MissionUser:
        """Обновить миссию для пользователя

        Args:
            obj (MissionUserUpdateDTO): Объект создания

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def list_for_user(
        self, *, filter_obj: MockObj, order_obj: MockObj, pagination_obj: MockObj
    ) -> list[MissionUser]:
        """Получить список миссий пользователя

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[MissionUser]: Список сущностей миссии пользователя
        """

    @abstractmethod
    async def get_for_user(self, *, id: int) -> MissionUser:
        """Получить миссию пользователя

        Args:
            id (int): ID миссии пользователя

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def create_for_community(self, *, obj: MissionCommunityCreateDTO) -> MissionCommunity:
        """Создать миссию для сообщест ва

        Args:
            obj (MissionCommunityCreateDTO): Объект создания

        Returns:
            MissionCommunity: Сущность миссии сообщества
        """

    @abstractmethod
    async def update_for_community(self, *, obj: MissionCommunityUpdateDTO) -> MissionCommunity:
        """Обновить миссию сообщества

        Args:
            obj (MissionCommunityUpdateDTO): Объект обновления

        Returns:
            MissionCommunity: Сущность миссии сообщества
        """

    @abstractmethod
    async def list_for_community(
        self, *, filter_obj: MockObj, order_obj: MockObj, pagination_obj: MockObj
    ) -> list[MissionCommunity]:
        """Получить список миссий сообщества

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[MissionCommunity]: Список сущностей миссии сообщества
        """

    @abstractmethod
    async def get_for_community(self, *, id: int) -> MissionCommunity:
        """Получить миссию сообщества

        Args:
            id (int): ID миссии сообщества

        Returns:
            MissionCommunity: Сущность миссии сообщества
        """
