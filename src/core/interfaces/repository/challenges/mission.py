from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.dto.challenges.mission import (
    MissionCommunityCreateDTO,
    MissionCommunityUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionCommunity, MissionUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


@dataclass
class MissionFilter:
    active: bool | None = None


@dataclass
class MissionUserFilter:
    mission_id: int | None = None
    status: OccupancyStatusEnum | None = None


@dataclass
class MissionCommunityFilter:
    community_id: int | None = None
    community_id_list: list[int] | None = None
    mission_id: int | None = None
    status: OccupancyStatusEnum | None = None


class IRepositoryMission(ABC):
    @abstractmethod
    async def get(self, *, id: int, lang: LanguageEnum) -> Mission:
        """Получить базовую миссию

        Args:
            id (int): ID базовой миссии
            lang (LanguageEnum): Необходимый язык

        Returns:
            MissionBase: Сущность базовой миссии

        Raises:
            EntityNotFound - Сущность не найдена
            TranslateNotFound - Не найден перевод
        """

    @abstractmethod
    async def lst(
        self, *, filter_obj: MissionFilter, order_obj: MockObj, pagination_obj: MockObj, lang: LanguageEnum
    ) -> list[Mission]:
        """Получить список базовых миссий

        Args:
            filter_obj (MissionFilter): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации
            lang (LanguageEnum): Необходимый язык

        Returns:
            List[MissionBase]: Список базовых миссий
        """

    @abstractmethod
    async def user_mission_get(self, *, id: int, user_id: int) -> MissionUser:
        """Получить миссию пользователя

        Args:
            id (int): ID Сущности миссии пользователя

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def user_mission_create(self, *, user_id: int, obj: MissionUserCreateDTO) -> MissionUser:
        """Создать миссию для пользователя

        Args:
            obj (MissionUserCreateDTO): Объект создания

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def user_mission_update(self, *, id: int, user_id: int, obj: MissionUserUpdateDTO) -> MissionUser:
        """Обновить миссию для пользователя

        Args:
            id (int): ID Сущности миссии пользователя

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def user_mission_lst(
        self,
        *,
        user_id: int,
        filter_obj: MissionUserFilter,
        order_obj: MockObj,
        pagination_obj: MockObj,
    ) -> list[MissionUser]:
        """Получить список миссий пользователя

        Args:
            filter_obj (MissionUserFilter): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[MissionUser]: Список сущностей миссии пользователя
        """

    @abstractmethod
    async def community_mission_create(self, *, community_id: int, obj: MissionCommunityCreateDTO) -> MissionCommunity:
        """Создать миссию для сообщест ва

        Args:
            obj (MissionCommunityCreateDTO): Объект создания

        Returns:
            MissionCommunity: Сущность миссии сообщества
        """

    @abstractmethod
    async def community_mission_get(self, *, id: int, community_id: int) -> MissionCommunity:
        """Получить миссию сообщества

        Args:
            id (int): ID Сущности миссии сообщества
            community_id (int): ID сообщества

        Returns:
            MissionCommunity: Сущность миссии сообщества
        """

    @abstractmethod
    async def community_mission_update(
        self, *, id: int, community_id: int, obj: MissionCommunityUpdateDTO
    ) -> MissionCommunity:
        """Обновить миссию сообщества

        Args:
            id (int): ID Сущности миссии сообщества
            obj (MissionCommunityUpdateDTO): Объект обновления

        Returns:
            MissionCommunity: Сущность миссии сообщества
        """

    @abstractmethod
    async def community_mission_lst(
        self,
        *,
        filter_obj: MissionCommunityFilter,
        order_obj: MockObj,
        pagination_obj: MockObj,
    ) -> list[MissionCommunity]:
        """Получить список миссий сообщества

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[MissionCommunity]: Список сущностей миссии сообщества
        """
