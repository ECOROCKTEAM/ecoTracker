from abc import ABC, abstractmethod
from typing import List
from backend.src.core.dto.mock import MockObj

from backend.src.core.entity.mission import (
    Mission,
    MissionUpdateDTO,
    MissionCreateDTO,
    MissionUserCreateDTO,
    MisssionUser,
    MissionUserUpdateDTO,
    MissionCommunity,
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
)


class IRepositoryMission(ABC):
    @abstractmethod
    async def get(self, *, id: int) -> Mission:
        """Получить базовую миссию

        Args:
            id (int): ID базовой миссии

        Returns:
            Mission: Сущность базовой миссии

        """

    @abstractmethod
    async def update(self, *, obj: MissionUpdateDTO) -> Mission:
        """Обновить базовую миссию

        Args:
            obj (MissionUpdateDTO): Объект обновления

        Returns:
            Mission: Сущность безовой миссии
        """

    @abstractmethod
    async def create(self, *, obj: MissionCreateDTO) -> Mission:
        """Создать базовую миссию

        Args:
            obj (MissionCreateDTO): Объект создания

        Returns:
            Mission: Сущность безовой миссии
        """

    @abstractmethod
    async def list(self, *, filter_obj: MockObj, order_obj: MockObj, pagination_obj: MockObj) -> List[Mission]:
        """Получить список базовых миссий

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[Mission]: Список базовых миссий
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
    async def create_for_user(self, *, obj: MissionUserCreateDTO) -> MisssionUser:
        """Создать миссию для пользователя

        Args:
            obj (MissionUserCreateDTO): Объект создания

        Returns:
            MisssionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def update_for_user(self, *, obj: MissionUserUpdateDTO) -> MisssionUser:
        """Обновить миссию для пользователя

        Args:
            obj (MissionUserUpdateDTO): Объект создания

        Returns:
            MisssionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def list_for_user(self, *, filter_obj: MockObj, order_obj: MockObj, pagination_obj: MockObj) -> List[MisssionUser]:
        """Получить список миссий пользователя

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[MisssionUser]: Список сущностей миссии пользователя
        """

    @abstractmethod
    async def get_for_user(self, *, id: int) -> MisssionUser:
        """Получить миссию пользователя

        Args:
            id (int): ID миссии пользователя

        Returns:
            MisssionUser: Сущность миссии пользователя
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
    ) -> List[MissionCommunity]:
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
