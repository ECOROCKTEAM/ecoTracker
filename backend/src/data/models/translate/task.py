from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.holder import Base
from src.core.enum.language import LanguageEnum


class TaskTranslateModel(Base):
    __tablename__ = "task_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    language: Mapped[LanguageEnum]
