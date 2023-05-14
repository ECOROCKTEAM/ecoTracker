from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql import func
from src.application.database.base import Base
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum

if TYPE_CHECKING:
    from src.data.models.challenges.occupancy import OccupancyCategoryModel


@dataclass
class TaskModel(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    score: Mapped[int]  # type: ignore
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))

    category: Mapped["OccupancyCategoryModel"] = relationship(lazy="joined", back_populates="tasks")
    translations: Mapped[list["TaskTranslateModel"]] = relationship(lazy="selectin", back_populates="task")


@dataclass
class TaskTranslateModel(Base):
    __tablename__ = "task_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]  # type: ignore
    description: Mapped[str]  # type: ignore
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    language: Mapped[LanguageEnum]  # type: ignore

    task: Mapped["TaskModel"] = relationship(lazy="noload", back_populates="translations")


# @dataclass
# class UserTask(Base):
#     __tablename__ = "user_task"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
#     task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))


@dataclass
class UserTaskPlan(Base):
    __tablename__ = "user_task_plan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    date_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_close: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[OccupancyStatusEnum]  # type: ignore
