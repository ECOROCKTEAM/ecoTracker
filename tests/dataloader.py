import random
from abc import ABC, abstractmethod
from datetime import datetime
from functools import wraps
from random import randint
from typing import Generic, Type, TypeVar, get_args
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.group.role import GroupRoleEnum
from src.core.enum.language import LanguageEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.enum.user.contact import ContactTypeEnum
from src.data.models.challenges.mission import (
    GroupMissionModel,
    MissionModel,
    UserMissionModel,
)
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)
from src.data.models.challenges.task import TaskModel, TaskTranslateModel, UserTaskModel
from src.data.models.group.group import GroupModel
from src.data.models.user.user import (
    UserContactModel,
    UserGroupModel,
    UserModel,
    UserScoreModel,
)

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
        # print(f"{self.__class__.__name__} ADD: {pk_values}")
        return model

    async def _get(self, model: Type[T], cond: list) -> T | None:
        stmt = select(model)  # type: ignore
        stmt = stmt.where(*cond)
        coro = await self.session.scalars(stmt)
        result = coro.all()
        if len(result) == 0:
            return None
        if len(result) > 1:
            raise Exception("Wait one entity, get > 1")
        return result[0]

    @abstractmethod
    async def create(self) -> T:
        ...

    @abstractmethod
    async def get(self) -> T | None:
        ...


class UserScoreLoader(EntityLoaderBase[UserScoreModel]):
    async def create(
        self, user: UserModel, operation: ScoreOperationEnum | None = None, value: int | None = None
    ) -> UserScoreModel:
        if operation is None:
            operation = random.choice([ScoreOperationEnum.MINUS, ScoreOperationEnum.PLUS])
        if value is None:
            value = random.randint(50, 1000)
        model = UserScoreModel(user_id=user.id, operation=operation, value=value)
        return await self._add(model)

    async def get(self) -> UserScoreModel | None:
        return await super().get()  # type: ignore


class OccupancyCategoryTranslateLoader(EntityLoaderBase[OccupancyCategoryTranslateModel]):
    async def create(
        self, category: OccupancyCategoryModel, name: str | None = None, language: LanguageEnum = LanguageEnum.EN
    ) -> OccupancyCategoryTranslateModel:
        if name is None:
            name = uuid()
        model = OccupancyCategoryTranslateModel(name=name, language=language, category_id=category.id)
        return await self._add(model)

    async def get(self) -> OccupancyCategoryTranslateModel | None:
        return await super().get()  # type: ignore


class OccupancyCategoryLoader(EntityLoaderBase[OccupancyCategoryModel]):
    async def create(self) -> OccupancyCategoryModel:
        model = OccupancyCategoryModel()
        return await self._add(model)

    async def get(self, id: int) -> OccupancyCategoryModel | None:
        cond = []
        if id is not None:
            cond.append(OccupancyCategoryModel.id == id)
        return await self._get(OccupancyCategoryModel, cond)


class TaskTranslateLoader(EntityLoaderBase[TaskTranslateModel]):
    async def create(self) -> TaskTranslateModel:
        return await super().create()  # type: ignore

    async def get(self) -> TaskTranslateModel | None:
        return await super().get()  # type: ignore


class TaskLoader(EntityLoaderBase[TaskModel]):
    async def create(
        self,
        category: OccupancyCategoryModel,
        score: int | None = None,
        active: bool = True,
    ) -> TaskModel:
        if score is None:
            score = random.randint(50, 1000)
        model = TaskModel(score=score, active=active, category_id=category.id)
        return await self._add(model)

    async def get(
        self,
        id: int | None = None,
        active: bool | None = None,
    ) -> TaskModel | None:
        cond = []
        if id is not None:
            cond.append(TaskModel.id == id)
        if active is not None:
            cond.append(TaskModel.active.is_(active))
        return await self._get(TaskModel, cond)


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


class UserContactLoader(EntityLoaderBase[UserContactModel]):
    async def create(
        self,
        id: int | None = None,
        user_id: str | None = None,
        value: str = "test@gmail.com",
        type: ContactTypeEnum = ContactTypeEnum.GMAIL,
        active: bool = True,
        is_favorite: bool = True,
    ) -> UserContactModel:
        model = UserContactModel(
            id=id,
            user_id=user_id or uuid(),
            value=value,
            type=type,
            active=active,
            is_favorite=is_favorite,
        )
        return await self._add(model=model)

    async def get(self, id: int | None = None) -> UserContactModel | None:
        cond = []
        if id is not None:
            cond.append(UserContactModel.id == id)
        return await self._get(model=UserContactModel, cond=cond)


class UserLoader(EntityLoaderBase[UserModel]):
    async def create(
        self,
        id: str | None = None,
        username: str | None = None,
        active: bool = True,
        language: LanguageEnum = LanguageEnum.EN,
    ) -> UserModel:
        model = UserModel(id=id or uuid(), username=username or uuid(), active=active, language=language)
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


class UserTaskLoader(EntityLoaderBase[UserTaskModel]):
    async def create(
        self,
        user_id: str,
        task_id: int,
        status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE,
        date_start: datetime = datetime.now(),
        date_close: datetime | None = None,
    ) -> UserTaskModel:
        model = UserTaskModel(
            user_id=user_id, task_id=task_id, status=status, date_start=date_start, date_close=date_close
        )
        return await self._add(model=model)

    async def get(
        self,
        user_id: str | None = None,
        task_id: int | None = None,
        status: OccupancyStatusEnum | None = None,
    ) -> UserTaskModel | None:
        cond = []
        if user_id is not None:
            cond.append(UserTaskModel.user_id == user_id)
        if task_id is not None:
            cond.append(UserTaskModel.task_id == task_id)
        if status is not None:
            cond.append(UserTaskModel.status == status)
        return await self._get(model=UserTaskModel, cond=cond)


class MissionLoader(EntityLoaderBase[MissionModel]):
    async def create(self, category_id: int, active: bool | None = None, score: int | None = None) -> MissionModel:
        model = MissionModel(category_id=category_id, active=active or True, score=score or 10)
        return await self._add(model=model)

    async def get(
        self, active: bool = True, author: str | None = None, category_id: int | None = None
    ) -> MissionModel | None:
        cond = []
        if active is not None:
            cond.append(MissionModel.active == active)
        if category_id is not None:
            cond.append(MissionModel.category_id == category_id)
        return await self._get(model=MissionModel, cond=cond)


class GroupMissionLoader(EntityLoaderBase[GroupMissionModel]):
    async def create(
        self, group_id: int, mission_id: int, author: str, status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE
    ) -> GroupMissionModel:
        model = GroupMissionModel(mission_id=mission_id, group_id=group_id, author=author, status=status)
        return await self._add(model=model)

    async def get(
        self,
        author: str | None = None,
        mission_id: int | None = None,
        group_id: int | None = None,
        status: OccupancyStatusEnum | None = None,
    ) -> GroupMissionModel | None:
        cond = []
        if author is not None:
            cond.append(GroupMissionModel.author == author)
        if mission_id is not None:
            cond.append(GroupMissionModel.mission_id)
        if group_id is not None:
            cond.append(GroupMissionModel.group_id == group_id)
        if status is not None:
            cond.append(GroupMissionModel.status == status)
        return await self._get(model=GroupMissionModel, cond=cond)


class UserMissionLoader(EntityLoaderBase[UserMissionModel]):
    async def create(
        self,
        user_id: str,
        mission_id: int,
        status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE,
        date_start: datetime = datetime.now(),
    ) -> UserMissionModel:
        model = UserMissionModel(user_id=user_id, mission_id=mission_id, status=status, date_start=date_start)
        return await self._add(model=model)

    async def get(
        self,
        user_id: str | None = None,
        mission_id: int | None = None,
        status: OccupancyStatusEnum | None = None,
    ) -> UserMissionModel | None:
        cond = []
        if user_id is not None:
            cond.append(UserMissionModel.user_id == user_id)
        if mission_id is not None:
            cond.append(UserMissionModel.mission_id == mission_id)
        if status is not None:
            cond.append(UserMissionModel.status == status)
        return await self._get(model=UserMissionModel, cond=cond)


def loader_track(func):
    @wraps(func)
    def wrapper(self):
        func_name = func.__name__
        if func_name not in self._loader_instance_holder:
            self._loader_call_stack.append(func_name)
            loader = func(self)
            self._loader_instance_holder[func_name] = loader
        selected_instance = self._loader_instance_holder[func_name]
        # print(f"Ret {func_name=} {id(selected_instance)}")
        return selected_instance

    return wrapper


class dataloader:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._loader_call_stack = []
        self._loader_instance_holder = {}

    async def __aenter__(self):
        print()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # print()
        await self.delete_created_all()

    async def delete_created_all(self):
        await self.session.rollback()
        for loader_name in reversed(self._loader_call_stack):
            instance = self._loader_instance_holder[loader_name]
            await instance._delete_created()
            # print(f"{instance.__class__.__name__} -> deleted count {len(instance._create_stack)}")

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    @property
    @loader_track
    def user_contact_loader(self) -> UserContactLoader:
        return UserContactLoader(session=self.session)

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

    @property
    @loader_track
    def task_loader(self) -> TaskLoader:
        return TaskLoader(session=self.session)

    @property
    @loader_track
    def user_task_loader(self) -> UserTaskLoader:
        return UserTaskLoader(session=self.session)

    @property
    @loader_track
    def mission_loader(self) -> MissionLoader:
        return MissionLoader(session=self.session)

    @property
    @loader_track
    def user_mission_loader(self) -> UserMissionLoader:
        return UserMissionLoader(session=self.session)

    @property
    @loader_track
    def group_mission_loader(self) -> GroupMissionLoader:
        return GroupMissionLoader(session=self.session)

    @property
    @loader_track
    def task_translate_loader(self) -> TaskTranslateLoader:
        return TaskTranslateLoader(session=self.session)

    @property
    @loader_track
    def category_loader(self) -> OccupancyCategoryLoader:
        return OccupancyCategoryLoader(session=self.session)

    @property
    @loader_track
    def category_translate_loader(self) -> OccupancyCategoryTranslateLoader:
        return OccupancyCategoryTranslateLoader(session=self.session)

    @property
    @loader_track
    def user_score_loader(self) -> UserScoreLoader:
        return UserScoreLoader(session=self.session)

    async def create_category(
        self, name: str | None = None, language_list: list[LanguageEnum] | None = None
    ) -> OccupancyCategoryModel:
        if language_list is None:
            language_list = [LanguageEnum.EN]
        category = await self.category_loader.create()
        for lang in language_list:
            await self.category_translate_loader.create(category=category, name=name, language=lang)
        return category
