from abc import ABC, abstractmethod
from typing import List
from backend.src.core.dto.mock import MockObj

from src.core.dto.community.filters import (
    CommunityIncludeUserFilter,
    CommunityListFilter,
)
from src.core.dto.community.invite import (
    CommunityInviteCreateDTO,
    CommunityInviteDTO,
    CommunityInviteUpdateDTO,
)
from src.core.dto.community.role import CommunityRoleCreateDTO, CommunityRoleDTO
from src.core.dto.community.privacy import PrivacyCreateDTO, PrivacyDTO
from src.core.dto.m2m.user.community import (
    UserCommunityDTO,
    UserCommunityCreateDTO,
    UserCommunityUpdateDTO,
)
from src.core.entity.community import Community, CommunityCreateDTO, CommunityUpdateDTO
from src.core.enum.community.role import CommunityRoleEnum

class IRepositoryCommunity(ABC):

    @abstractmethod
    async def get(self, *, id: str) -> Community:
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
    async def update(self, *, id: str, obj: CommunityUpdateDTO) -> Community:
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
    async def list(self, *, obj: CommunityListFilter, order_obj: MockObj, pagination_obj: MockObj) -> List[Community]:
        """Получить список сообществ

        Args:
            obj (CommunityListFilter): DTO фильтрации сообщества

        Returns:
            List[Community]: Список сущностей сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def deactivate(self, *, id: str) -> str:
        """Удалить сообщество (Soft delete)

        Args:
            id (str): Id сообщества

        Returns:
            str: Id удалённого сообщества

        Raises:
            RepoError: Ошибка операции
            CommunityDeleteError: Ошибка при удалении сообщества
        """
    

    @abstractmethod
    async def privacy_create(self, *, obj: PrivacyCreateDTO) -> PrivacyDTO:
        """Добавить тип приватности для сообщества

        Args:
            create_obj (PrivacyCreateDTO): DTO объект создания типа приватности

        Returns:
            PrivacyDTO: Типов приватности для сообщества

        Raises:
            RepoError: Ошибка операции
        """
    
    @abstractmethod
    async def privacy_list(self) -> List[PrivacyDTO]:
        """Получить список типов приватности для сообщества

        Returns:
            List[PrivacyListDTO]: Список типов приватности для сообщества

        Raises:
            RepoError: Ошибка операции
        """
    
    @abstractmethod
    async def role_get(
        self, *, enum: CommunityRoleEnum
    ) -> CommunityRoleDTO:
        """Получить роль сообщества

        Args:
            enum (CommunityRoleEnum): Элемент перечисления CommunityRoleEnum

        Returns:
            CommunityRoleDTO: Роль сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def role_create(
        self, *, obj: CommunityRoleCreateDTO
    ) -> CommunityRoleDTO:
        """Создать роль для сообщества

        Args:
            obj (CommunityRoleCreateDTO): DTO объект создания роли сообщества

        Returns:
            CommunityRoleDTO: Роль сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def role_list(self) -> List[CommunityRoleDTO]:
        """Получить список ролей для сообщества

        Returns:
            List[CommunityRoleDTO]: Список ролей для сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def user_add(
        self, *, obj: UserCommunityCreateDTO
    ) -> UserCommunityDTO:
        """Добавить пользователя в сообщество

        Args:
            obj (UserCommunityCreateDTO): DTO объект создания связи между пользователем и сообществом

        Returns:
            UserCommunityDTO: Объект связи пользователя и сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def user_get(self, *, id: int) -> UserCommunityDTO:
        """Получить связь сообщество-пользователь

        Args:
            id (int): Id связи

        Returns:
            UserCommunityDTO: Объект связи пользователя и сообщества

        Raises:
            RepoError: Ошибка операции
            UserNotInCommunity: Связь не найдена
        """

    @abstractmethod
    async def user_list(
        self, *, id: str, filter: CommunityIncludeUserFilter
    ) -> List[UserCommunityDTO]:
        """Получить список ID пользователей входящих в сообщество

        Args:
            id (str): ID сообщества
            filter (CommunityIncludeUserListFilter): DTO объект фильтрации

        Returns:
            List[UserCommunityDTO]: Список связей пользователей

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def user_role_update(
        self, *, obj: UserCommunityUpdateDTO
    ) -> UserCommunityDTO:
        """Обновить роль пользователя в сообществе

        Args:
            obj (UserCommunityUpdateDTO): DTO объект обновления роли пользователя в сообществе

        Returns:
            UserCommunityDTO: Объект связи пользователя и сообщества

        Raises:
            RepoError: Ошибка операции
            UserNotInCommunity: Связь не найдена
        """

    @abstractmethod
    async def invite_link_create(
        self, *, obj: CommunityInviteCreateDTO
    ) -> CommunityInviteDTO:
        """Создать инвайт ссылку сообщества

        Args:
            obj (CommunityInviteCreateDTO): DTO объект создания ссылки для сообщества

        Returns:
            CommunityInviteDTO: DTO объект ссылки сообщества

        Raises:
            RepoError: Ошибка операции
        """

    @abstractmethod
    async def invite_link_get(
        self, *, id: str
    ) -> CommunityInviteDTO:
        """Получить инвайт ссылку

        Args:
            str (id): Id сообщества

        Returns:
            CommunityInviteDTO: DTO объект ссылки сообщества

        Raises:
            RepoError: Ошибка операции
            CommunityInviteLinkNotFoundError: Ссылка не найдена
        """

    @abstractmethod
    async def invite_link_update(
        self, *, obj: CommunityInviteUpdateDTO
    ) -> CommunityInviteDTO:
        """Обновить инвайт ссылку на сообщество

        Args:
            obj (CommunityInviteUpdateDTO): DTO объект обновления ссылки для сообщества

        Returns:
            CommunityInviteDTO: DTO объект ссылки сообщества

        Raises:
            RepoError: Ошибка операции
        """
