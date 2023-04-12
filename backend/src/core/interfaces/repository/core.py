from abc import ABC, abstractmethod
from typing import List
from src.core.dto.community import CommunityIncludeUserFilter, CommunityListFilter
from src.core.dto.community_role import CommunityRoleCreateDTO, CommunityRoleDTO
from src.core.dto.privacy import PrivacyCreateDTO, PrivacyDTO
from src.core.dto.shared import UserCommunityDTO, UserCommunityCreateDTO

from src.core.entity.user import User
from src.core.entity.community import Community, CommunityCreateDTO, CommunityUpdateDTO


class IRepositoryCore(ABC):
    @abstractmethod
    async def user_get(self, *, id: str) -> User:
        """Получить пользователя по id

        Args:
            id (str): Id пользователя

        Returns:
            User: Сущность пользователя

        Raises:
            RepoError: Ошибка операции
            UserNotFoundError: Пользователь не найден
        """

    @abstractmethod
    async def community_get(self, *, id: str) -> Community:
        """Получить сообщество по id

        Args:
            id (str): Id сообщества

        Returns:
            Community: Сущность сообщества

        Raises:
            RepoError: Ошибка операции
            CommunityNotFoundError: Сообщество не найдено
        """

    @abstractmethod
    async def community_create(self, *, obj: CommunityCreateDTO) -> Community:
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
    async def community_update(self, *, id: str, obj: CommunityUpdateDTO) -> Community:
        """Обновить поля сообщества

        Args:
            id (str): Id сообщества
            obj (CommunityUpdateDTO): DTO обновления сообщества

        Returns:
            Community: Сущность сообщества

        Raises:
            RepoError: Ошибка операции
            CommunityUpdateError: Ошибка при обновлении сообщества
        """

    @abstractmethod
    async def community_list(self, *, obj: CommunityListFilter) -> list[Community]:
        """Получить список сообществ

        Args:
            obj (CommunityListFilter): DTO фильтрации сообщества

        Returns:
            list[Community]: Список сущностей сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def community_delete(self, *, id: str) -> int:
        """Удалить сообщество

        Args:
            id (str): Id сообщества

        Returns:
            int: Id удалённого сообщества

        Raises:
            RepoError: Ошибка операции
            CommunityDeleteError: Ошибка при удалении сообщества
        """

    @abstractmethod
    async def community_user_ids(self, *, id: str, filter: CommunityIncludeUserFilter) -> list[str]:
        """Получить список ID пользователей входящих в сообщество

        Args:
            id (str): ID сообщества
            filter (CommunityIncludeUserListFilter): DTO объект фильтрации

        Returns:
            List[int]: Список ID пользователей

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def community_privacy_create(self, *, obj: PrivacyCreateDTO) -> PrivacyDTO:
        """Добавить тип приватности для сообщества

        Args:
            create_obj (PrivacyCreateDTO): DTO объект создания типа приватности

        Returns:
            PrivacyDTO: Типов приватности для сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def community_privacy_list(self) -> list[PrivacyDTO]:
        """Получить список типов приватности для сообщества

        Returns:
            list[PrivacyListDTO]: Список типов приватности для сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def community_role_create(self, *, obj: CommunityRoleCreateDTO) -> CommunityRoleDTO:
        """Создать роль для сообщества

        Args:
            obj (CommunityRoleCreateDTO): DTO объект создания роли сообщества

        Returns:
            CommunityRoleDTO: Роль сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def community_role_list(self) -> list[CommunityRoleDTO]:
        """Получить список ролей для сообщества

        Returns:
            list[CommunityRoleDTO]: Список ролей для сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def community_add_user(self, *, obj: UserCommunityCreateDTO) -> UserCommunityDTO:
        """Добавить пользователя в сообщество

        Args:
            obj (UserCommunityCreateDTO): DTO объект создания связи между пользователем и сообществом

        Returns:
            UserCommunityDTO: Объект связи пользователя и сообщества

        Raises:
            RepoError: Ошибка операции
        """
