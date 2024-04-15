from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.dto.challenges.mission import (
    MissionGroupCreateDTO,
    MissionGroupUpdateDTO,
    MissionUserCreateDTO,
    MissionUserUpdateDTO,
)
from src.core.dto.utils import IterableObj, Pagination, SortObj
from src.core.entity.mission import Mission, MissionGroup, MissionUser
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


@dataclass
class SortMissionObj(SortObj):
    ...


@dataclass
class SortUserMissionObj(SortObj):
    field: str = "mission_id"


@dataclass
class SortGroupMissionObj(SortObj):
    field: str = "mission_id"


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
        self, *, filter_obj: MissionFilter, sorting_obj: SortMissionObj, iterable_obj: IterableObj, lang: LanguageEnum
    ) -> Pagination[list[Mission]]:
        """Получить список базовых миссий

        Args:
            filter_obj (MissionFilter): Объект фильтрации
            sorting_obj (SortMissionObj): Объект сортировки
            iterable_obj (IterableObj): Объект пагинации
            lang (LanguageEnum): Необходимый язык

        Returns:
            Pagination[list[Mission]]: list of Mission entities
        """

    @abstractmethod
    async def user_mission_get(self, *, id: int, user_id: str) -> MissionUser:
        """Получить миссию пользователя

        Args:
            id (int): ID Сущности миссии пользователя

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def user_mission_create(self, *, user_id: str, obj: MissionUserCreateDTO) -> MissionUser:
        """Создать миссию для пользователя

        Args:
            obj (MissionUserCreateDTO): Объект создания

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def user_mission_update(self, *, id: int, user_id: str, obj: MissionUserUpdateDTO) -> MissionUser:
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
        user_id: str,
        filter_obj: MissionUserFilter,
        sorting_obj: SortUserMissionObj,
        iterable_obj: IterableObj,
    ) -> Pagination[list[MissionUser]]:
        """Получить список миссий пользователя

        Args:
            filter_obj (MissionUserFilter): Объект фильтрации
            sorting_obj (SortUserMissionObj): Объект сортировки
            iterable_obj (IterableObj): Объект пагинации

        Returns:
            Pagination[list[MissionUser]]: Список сущностей миссии пользователя
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
        sorting_obj: SortGroupMissionObj,
        iterable_obj: IterableObj,
    ) -> Pagination[list[MissionGroup]]:
        """Получить список миссий сообщества

        Args:
            filter_obj (MissionGroupFilter): Объект фильтрации
            sorting_obj (SortGroupMissionObj): Объект порядка
            iterable_obj (IterableObj): Объект пагинации

        Returns:
            Pagination[list[MissionGroup]]: Список сущностей миссии сообщества
        """
