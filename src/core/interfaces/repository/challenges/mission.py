from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.dto.challenges.mission import (
    MissionGroupCreateDTO,
    MissionGroupUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.mission import Mission, MissionGroup, MissionUser
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
class MissionGroupFilter:
    group_id: int | None = None
    group_id_list: list[int] | None = None
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
    async def group_mission_create(self, *, group_id: int, obj: MissionGroupCreateDTO) -> MissionGroup:
        """Создать миссию для сообщест ва

        Args:
            obj (MissionGroupCreateDTO): Объект создания

        Returns:
            MissionGroup: Сущность миссии сообщества
        """

    @abstractmethod
    async def group_mission_get(self, *, id: int, group_id: int) -> MissionGroup:
        """Получить миссию сообщества

        Args:
            id (int): ID Сущности миссии сообщества
            group_id (int): ID сообщества

        Returns:
            MissionGroup: Сущность миссии сообщества
        """

    @abstractmethod
    async def group_mission_update(self, *, id: int, group_id: int, obj: MissionGroupUpdateDTO) -> MissionGroup:
        """Обновить миссию сообщества

        Args:
            id (int): ID Сущности миссии сообщества
            obj (MissionGroupUpdateDTO): Объект обновления

        Returns:
            MissionGroup: Сущность миссии сообщества
        """

    @abstractmethod
    async def group_mission_lst(
        self,
        *,
        filter_obj: MissionGroupFilter,
        order_obj: MockObj,
        pagination_obj: MockObj,
    ) -> list[MissionGroup]:
        """Получить список миссий сообщества

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[MissionGroup]: Список сущностей миссии сообщества
        """
