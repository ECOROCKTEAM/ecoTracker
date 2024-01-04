from abc import ABC, abstractmethod
from datetime import datetime
from functools import wraps
from typing import Any, Coroutine, Generic, Type, TypeVar, get_args
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.inspection import inspect

from src.application.database.base import (
    Base,
    create_async_engine,
    create_session_factory,
)
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.enum.language import LanguageEnum
from src.data.models.group.group import GroupModel
from src.data.models.user.user import UserGroupModel, UserModel

T = TypeVar("T")

uuid = lambda: str(uuid4())


class UnsetType:
    ...


UnsetVal = UnsetType()


class EntityLoaderBase(ABC, Generic[T]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        (self._model_cls,) = get_args(self.__class__.__orig_bases__[0])  # type: ignore
        self._pk_names = [pk.name for pk in inspect(self._model_cls).primary_key]
        self._create_stack = []

    async def _delete_created(self):
        converted_vals = {}
        for pk_value_map in self._create_stack:
            for pk_name, value in pk_value_map.items():
                if converted_vals.get(pk_name) is None:
                    converted_vals[pk_name] = []
                converted_vals[pk_name].append(value)
        condition = [getattr(self._model_cls, attr_name).in_(values) for attr_name, values in converted_vals.items()]
        stmt = delete(self._model_cls).where(*condition)
        await self.session.execute(stmt)
        await self.session.commit()

    async def _add(self, model: T) -> T:
        self.session.add(model)
        await self.session.commit()
        pk_values = {}
        for pk_name in self._pk_names:
            pk_values[pk_name] = getattr(model, pk_name)
        self._create_stack.append(pk_values)
        print(f"{self.__class__.__name__} ADD: {pk_values}")
        return model

    async def _get(self, model: Type[T], cond: list) -> T:
        stmt = select(model)  # type: ignore
        stmt = stmt.where(*cond)
        coro = await self.session.scalars(stmt)
        result = coro.all()
        if len(result) == 0:
            raise Exception("Wait one entity, get 0")
        if len(result) > 1:
            raise Exception("Wait one entity, get > 1")
        return result[0]

    @abstractmethod
    async def create(self) -> T:
        ...

    @abstractmethod
    async def get(self) -> T | None:
        ...


class GroupLoader(EntityLoaderBase[GroupModel]):
    async def create(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str = "",
        active: bool = True,
        privacy: GroupPrivacyEnum = GroupPrivacyEnum.PUBLIC,
        code: str | None = None,
        code_expire_time: datetime | None = None,
    ) -> GroupModel:
        model = GroupModel(
            id=id,  # type: ignore
            name=name or uuid(),
            description=description,
            active=active,
            privacy=privacy,
            code=code,
            code_expire_time=code_expire_time,
        )
        return await self._add(model)

    async def get(
        self,
        id: int | None = None,
        name: str | None = None,
        active: bool | None = None,
        privacy: GroupPrivacyEnum | None = None,
        code: str | None | UnsetType = UnsetVal,
    ) -> GroupModel | None:
        cond = []
        if id is not None:
            cond.append(GroupModel.id == id)
        if name is not None:
            cond.append(GroupModel.name == name)
        if active is not None:
            cond.append(GroupModel.active.is_(active))
        if privacy is not None:
            cond.append(GroupModel.privacy == privacy)
        if not isinstance(code, UnsetType):
            cond.append(GroupModel.code == code)
        return await self._get(GroupModel, cond)


class UserGroupLoader(EntityLoaderBase[UserGroupModel]):
    async def create(self, user_id: str, group_id: int, role: GroupRoleEnum) -> UserGroupModel:
        model = UserGroupModel(user_id=user_id, group_id=group_id, role=role)
        return await self._add(model)

    async def get(self, user_id: str, group_id: int, role: GroupRoleEnum) -> UserGroupModel | None:
        cond = []
        if user_id is not None:
            cond.append(UserGroupModel.user_id == user_id)
        if group_id is not None:
            cond.append(UserGroupModel.group_id == group_id)
        if role is not None:
            cond.append(UserGroupModel.role == role)
        return await self._get(UserGroupModel, cond)


class UserLoader(EntityLoaderBase[UserModel]):
    async def create(
        self,
        id: str | None = None,
        username: str | None = None,
        active: bool = True,
        language: LanguageEnum = LanguageEnum.EN,
    ) -> UserModel:
        model = UserModel(
            id=id or uuid(), username=username or uuid(), password=uuid(), active=active, language=language
        )
        return await self._add(model)

    async def get(
        self,
        id: str | None = None,
        username: str | None = None,
        active: bool | None = None,
        language: LanguageEnum | None = None,
    ) -> UserModel | None:
        cond = []
        if id is not None:
            cond.append(UserModel.id == id)
        if username is not None:
            cond.append(UserModel.username == username)
        if active is not None:
            cond.append(UserModel.active.is_(active))
        if language is not None:
            cond.append(UserModel.language == language)
        return await self._get(UserModel, cond)


def loader_track(func):
    @wraps(func)
    def wrapper(self):
        func_name = func.__name__
        if func_name not in self._loader_instance_holder:
            self._loader_call_stack.append(func_name)
            loader = func(self)
            self._loader_instance_holder[func_name] = loader
        selected_instance = self._loader_instance_holder[func_name]
        print(f"Ret {func_name=} {id(selected_instance)}")
        return selected_instance

    return wrapper


class dataloader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._loader_call_stack = []
        self._loader_instance_holder = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print()
        await self._delete_created_all()

    async def _delete_created_all(self):
        await self.session.rollback()
        for loader_name in reversed(self._loader_call_stack):
            instance = self._loader_instance_holder[loader_name]
            await instance._delete_created()
            print(f"{instance.__class__.__name__} -> deleted count {len(instance._create_stack)}")

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    @property
    @loader_track
    def group_loader(self) -> GroupLoader:
        return GroupLoader(session=self.session)

    @property
    @loader_track
    def user_group_loader(self) -> UserGroupLoader:
        return UserGroupLoader(session=self.session)

    @property
    @loader_track
    def user_loader(self) -> UserLoader:
        return UserLoader(session=self.session)
