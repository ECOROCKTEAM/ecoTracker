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
from src.core.enum.language import LanguageEnum


@dataclass
class MissionFilter:
    active: bool | None = None


@dataclass
class MissionUserFilter(MissionFilter):
    """"""


@dataclass
class MissionCommunityFilter(MissionFilter):
    """"""


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

    # Replaced to admin app
    # @abstractmethod
    # async def deactivate(self, *, id: int) -> int:
    #     """Отключить миссию

    #     Args:
    #         id (int): ID базовой миссии

    #     Returns:
    #         int: ID базовой миссии
    #     """

    @abstractmethod
    async def user_mission_get(self, *, id: int, lang: LanguageEnum) -> MissionUser:
        """Получить миссию пользователя

        Args:
            id (int): ID миссии пользователя
            lang (LanguageEnum): Необходимый язык

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def user_mission_create(self, *, obj: MissionUserCreateDTO, lang: LanguageEnum) -> MissionUser:
        """Создать миссию для пользователя

        Args:
            obj (MissionUserCreateDTO): Объект создания
            lang (LanguageEnum): Необходимый язык

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def user_mission_update(self, *, obj: MissionUserUpdateDTO, lang: LanguageEnum) -> MissionUser:
        """Обновить миссию для пользователя

        Args:
            obj (MissionUserUpdateDTO): Объект обновления
            lang (LanguageEnum): Необходимый язык

        Returns:
            MissionUser: Сущность миссии пользователя
        """

    @abstractmethod
    async def user_mission_lst(
        self,
        *,
        filter_obj: MissionUserFilter,
        order_obj: MockObj,
        pagination_obj: MockObj,
        lang: LanguageEnum,
    ) -> list[MissionUser]:
        """Получить список миссий пользователя

        Args:
            filter_obj (MissionUserFilter): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации
            lang (LanguageEnum): Необходимый язык

        Returns:
            List[MissionUser]: Список сущностей миссии пользователя
        """

    @abstractmethod
    async def community_mission_create(self, *, obj: MissionCommunityCreateDTO, lang: LanguageEnum) -> MissionCommunity:
        """Создать миссию для сообщест ва

        Args:
            obj (MissionCommunityCreateDTO): Объект создания
            lang (LanguageEnum): Необходимый язык

        Returns:
            MissionCommunity: Сущность миссии сообщества
        """

    @abstractmethod
    async def community_mission_get(self, *, id: int, lang: LanguageEnum) -> MissionCommunity:
        """Получить миссию сообщества

        Args:
            id (int): ID миссии сообщества
            lang (LanguageEnum): Необходимый язык

        Returns:
            MissionCommunity: Сущность миссии сообщества
        """

    @abstractmethod
    async def community_mission_update(self, *, obj: MissionCommunityUpdateDTO, lang: LanguageEnum) -> MissionCommunity:
        """Обновить миссию сообщества

        Args:
            obj (MissionCommunityUpdateDTO): Объект обновления
            lang (LanguageEnum): Необходимый язык

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
        lang: LanguageEnum,
    ) -> list[MissionCommunity]:
        """Получить список миссий сообщества

        Args:
            filter_obj (MockObj): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации
            lang (LanguageEnum): Необходимый язык

        Returns:
            List[MissionCommunity]: Список сущностей миссии сообщества
        """
