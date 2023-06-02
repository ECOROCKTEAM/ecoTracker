from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.core.dto.community.community import CommunityCreateDTO, CommunityUpdateDTO
from src.core.dto.community.invite import CommunityInviteDTO, CommunityInviteUpdateDTO
from src.core.dto.m2m.user.community import (
    UserCommunityCreateDTO,
    UserCommunityDTO,
    UserCommunityUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.community import Community
from src.core.enum.community.role import CommunityRoleEnum


@dataclass
class CommunityFilter:
    name: str | None = None
    active: bool | None = None
    user_id: int | None = None


@dataclass
class CommunityUserFilter:
    role_list: list[CommunityRoleEnum] | None = field(default_factory=list)


class IRepositoryCommunity(ABC):
    @abstractmethod
    async def get(self, *, id: int) -> Community:
        """Получить сообщество по id

        Args:
            id (int): Id сообщества

        Returns:
            Community: Сущность сообщества

        Raises:
            RepoError: Ошибка операции
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def create(self, *, obj: CommunityCreateDTO) -> Community:
        """Создать сообщество

        Args:
            obj (CommunityCreateDTO): DTO создания сообщества

        Returns:
            Community: Сущность сообщества

        Raises:
            RepoError: Ошибка операции
            CommunityCreateError: Ошибка при создании сообщества
        """
        pass

    @abstractmethod
    async def update(self, *, id: int, obj: CommunityUpdateDTO) -> Community:
        """Обновить поля сообщества

        Args:
            id (int): Id сообщества
            obj (CommunityUpdateDTO): DTO обновления сообщества

        Returns:
            Community: Сущность сообщества

        Raises:
            RepoError: Ошибка операции
            CommunityUpdateError: Ошибка при обновлении сообщества
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def lst(self, *, filter_obj: CommunityFilter, order_obj: MockObj, pagination_obj: MockObj) -> list[Community]:
        """Получить список сообществ

        Args:
            filter_obj (CommunityFilter): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[Community]: Список сущностей сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def deactivate(self, *, id: int) -> int:
        """Удалить сообщество (Soft delete)

        Args:
            id (int): Id сообщества

        Returns:
            int: Id удалённого сообщества

        Raises:
            RepoError: Ошибка операции
            CommunityDeleteError: Ошибка при удалении сообщества
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def user_add(self, *, obj: UserCommunityCreateDTO) -> UserCommunityDTO:
        """Добавить пользователя в сообщество

        Args:
            obj (UserCommunityCreateDTO): DTO объект создания связи между пользователем и сообществом

        Returns:
            UserCommunityDTO: Объект связи пользователя и сообщества

        Raises:
            EntityNotFound: Сущность не найдена
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def user_get(
        self,
        *,
        community_id: int,
        user_id: int,
    ) -> UserCommunityDTO:
        """Получить связь сообщество-пользователь
        Args:
            user_id (int): Id пользователя
            community_id: Id сообщества
        Returns:
            UserCommunityDTO: Объект связи пользователя и сообщества
        Raises:
            RepoError: Ошибка операции
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def user_list(self, *, id: int, filter_obj: CommunityUserFilter) -> list[UserCommunityDTO]:
        """Получить список ID пользователей входящих в сообщество

        Args:
            id (int): ID сообщества
            filter_obj (CommunityUserFilter): DTO объект фильтрации

        Returns:
            List[UserCommunityDTO]: Список связей пользователей

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def user_role_update(
        self, *, community_id: int, user_id: int, obj: UserCommunityUpdateDTO
    ) -> UserCommunityDTO:
        """Обновить роль пользователя в сообществе

        Args:
            user_id (int): Id пользователя
            community_id: Id сообщества
            obj (UserCommunityUpdateDTO): DTO объект обновления роли пользователя в сообществе

        Returns:
            UserCommunityDTO: Объект связи пользователя и сообщества

        Raises:
            RepoError: Ошибка операции
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def user_remove(
        self,
        *,
        community_id: int,
        user_id: int,
    ) -> bool:
        """Удалить пользователя из сообщества

        Args:
            user_id (int): Id пользователя
            community_id: Id сообщества

        Returns:
            bool: статус операции

        Raises:
            RepoError: Ошибка операции
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def code_set(self, *, id: int, obj: CommunityInviteUpdateDTO) -> CommunityInviteDTO:
        """Обновить инвайт код сообщества

        Args:
            id (int): Id сообщества
            obj (CommunityInviteUpdateDTO): DTO объект обновления ссылки для сообщества

        Returns:
            CommunityInviteDTO: DTO объект ссылки сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def code_get(self, *, id: int) -> CommunityInviteDTO:
        """Получить инвайт код

        Args:
            id (int): Id сообщества

        Returns:
            CommunityInviteDTO: DTO объект ссылки сообщества

        Raises:
            EntityNotFound: Сущность не найдена
            RepoError: Ошибка операции
            CommunityInviteLinkNotFoundError: Ссылка не найдена
        """

    @abstractmethod
    async def get_by_code(self, code: str) -> Community:
        """Получить сообщество по коду

        Args:
            code (str): Код сообщества

        Returns:
            Community: Сущность сообщества

        Raises:
            EntityNotFound: Сущность не найдена
            RepoError: Ошибка операции
        """
