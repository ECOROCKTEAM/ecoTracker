from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.core.dto.group.group import GroupCreateDTO, GroupUpdateDTO
from src.core.dto.group.invite import GroupInviteDTO, GroupInviteUpdateDTO
from src.core.dto.m2m.user.group import (
    UserGroupCreateDTO,
    UserGroupDTO,
    UserGroupUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.group import Group
from src.core.enum.group.role import GroupRoleEnum


@dataclass
class GroupFilter:
    active: bool | None = None
    user_id: int | None = None


@dataclass
class GroupUserFilter:
    role_list: list[GroupRoleEnum] | None = field(default_factory=list)
    user_id__in: list[int] | None = None


class IRepositoryGroup(ABC):
    @abstractmethod
    async def get(self, *, id: int) -> Group:
        """Получить сообщество по id

        Args:
            id (int): Id сообщества

        Returns:
            Group: Сущность сообщества

        Raises:
            RepoError: Ошибка операции
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def create(self, *, obj: GroupCreateDTO) -> Group:
        """Создать сообщество

        Args:
            obj (GroupCreateDTO): DTO создания сообщества

        Returns:
            Group: Сущность сообщества

        Raises:
            RepoError: Ошибка операции
            GroupCreateError: Ошибка при создании сообщества
        """
        pass

    @abstractmethod
    async def update(self, *, id: int, obj: GroupUpdateDTO) -> Group:
        """Обновить поля сообщества

        Args:
            id (int): Id сообщества
            obj (GroupUpdateDTO): DTO обновления сообщества

        Returns:
            Group: Сущность сообщества

        Raises:
            RepoError: Ошибка операции
            GroupUpdateError: Ошибка при обновлении сообщества
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def lst(self, *, filter_obj: GroupFilter, order_obj: MockObj, pagination_obj: MockObj) -> list[Group]:
        """Получить список сообществ

        Args:
            filter_obj (GroupFilter): Объект фильтрации
            order_obj (MockObj): Объект порядка
            pagination_obj (MockObj): Объект пагинации

        Returns:
            List[Group]: Список сущностей сообщества

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
            GroupDeleteError: Ошибка при удалении сообщества
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def user_add(self, *, obj: UserGroupCreateDTO) -> UserGroupDTO:
        """Добавить пользователя в сообщество

        Args:
            obj (UserGroupCreateDTO): DTO объект создания связи между пользователем и сообществом

        Returns:
            UserGroupDTO: Объект связи пользователя и сообщества

        Raises:
            EntityNotFound: Сущность не найдена
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def user_get(
        self,
        *,
        group_id: int,
        user_id: int,
    ) -> UserGroupDTO:
        """Получить связь сообщество-пользователь
        Args:
            user_id (int): Id пользователя
            group_id: Id сообщества
        Returns:
            UserGroupDTO: Объект связи пользователя и сообщества
        Raises:
            RepoError: Ошибка операции
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def user_list(self, *, id: int, filter_obj: GroupUserFilter) -> list[UserGroupDTO]:
        """Получить список ID пользователей входящих в сообщество

        Args:
            id (int): ID сообщества
            filter_obj (GroupUserFilter): DTO объект фильтрации

        Returns:
            List[UserGroupDTO]: Список связей пользователей

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def user_role_update(self, *, group_id: int, user_id: int, obj: UserGroupUpdateDTO) -> UserGroupDTO:
        """Обновить роль пользователя в сообществе

        Args:
            user_id (int): Id пользователя
            group_id: Id сообщества
            obj (UserGroupUpdateDTO): DTO объект обновления роли пользователя в сообществе

        Returns:
            UserGroupDTO: Объект связи пользователя и сообщества

        Raises:
            RepoError: Ошибка операции
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def user_remove(
        self,
        *,
        group_id: int,
        user_id: int,
    ) -> bool:
        """Удалить пользователя из сообщества

        Args:
            user_id (int): Id пользователя
            group_id: Id сообщества

        Returns:
            bool: статус операции

        Raises:
            RepoError: Ошибка операции
            EntityNotFound: Сущность не найдена
        """

    @abstractmethod
    async def code_set(self, *, id: int, obj: GroupInviteUpdateDTO) -> GroupInviteDTO:
        """Обновить инвайт код сообщества

        Args:
            id (int): Id сообщества
            obj (GroupInviteUpdateDTO): DTO объект обновления ссылки для сообщества

        Returns:
            GroupInviteDTO: DTO объект ссылки сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def code_get(self, *, id: int) -> GroupInviteDTO:
        """Получить инвайт код

        Args:
            id (int): Id сообщества

        Returns:
            GroupInviteDTO: DTO объект ссылки сообщества

        Raises:
            EntityNotFound: Сущность не найдена
            RepoError: Ошибка операции
            GroupInviteLinkNotFoundError: Ссылка не найдена
        """

    @abstractmethod
    async def get_by_code(self, code: str) -> Group:
        """Получить сообщество по коду

        Args:
            code (str): Код сообщества

        Returns:
            Group: Сущность сообщества

        Raises:
            EntityNotFound: Сущность не найдена
            RepoError: Ошибка операции
        """
