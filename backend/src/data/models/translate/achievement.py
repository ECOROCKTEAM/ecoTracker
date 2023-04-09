from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.database.holder import Base
from src.core.enum.language import LanguageEnum


class AchievementTranslateModel(Base):
    __tablename__ = "achievement_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievement.id"))
    language: Mapped[LanguageEnum]


class AchievementCategoryTranslateModel(Base):
    __tablename__ = "achievement_category_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("achievement_category.id"))
    language: Mapped[LanguageEnum]


class AchievementProgressStatusTranslateModel(Base):
    __tablename__ = "achievement_progress_status_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    status_id: Mapped[int] = mapped_column(ForeignKey("achievement_progress_status.id"))
    language: Mapped[LanguageEnum]
