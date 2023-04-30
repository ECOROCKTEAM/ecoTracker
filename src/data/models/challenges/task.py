from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.application.database.base import Base
from src.core.enum.language import LanguageEnum


@dataclass
class TaskModel(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    score: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))


@dataclass
class TaskTranslateModel(Base):
    __tablename__ = "task_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    language: Mapped[LanguageEnum]
