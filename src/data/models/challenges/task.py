from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    score: Mapped[int] = mapped_column()
    active: Mapped[bool] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))

    category: Mapped["OccupancyCategoryModel"] = relationship(lazy="joined", back_populates="tasks")
    translations: Mapped[list["TaskTranslateModel"]] = relationship(lazy="selectin", back_populates="task")


@dataclass
class TaskTranslateModel(Base):
    __tablename__ = "task_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    language: Mapped[LanguageEnum] = mapped_column()

    task: Mapped["TaskModel"] = relationship(lazy="noload", back_populates="translations")


@dataclass
class UserTaskModel(Base):
    __tablename__ = "user_task"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True, nullable=False, autoincrement=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), primary_key=True, nullable=False, autoincrement=False)
    date_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_close: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[OccupancyStatusEnum] = mapped_column()


@dataclass
class UserTaskPlanModel(Base):
    __tablename__ = "user_task_plan"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True, nullable=False, autoincrement=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), primary_key=True, nullable=False, autoincrement=False)
