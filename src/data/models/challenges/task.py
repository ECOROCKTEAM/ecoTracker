from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.language import LanguageEnum


@dataclass
class TaskModel(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    score: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))


@dataclass
class TaskTranslateModel(Base):
    __tablename__ = "task_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    language: Mapped[LanguageEnum] = mapped_column()


@dataclass
class UserTaskPlan(Base):
    __tablename__ = "user_task_plan"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True, nullable=False, autoincrement=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), primary_key=True, nullable=False, autoincrement=False)
