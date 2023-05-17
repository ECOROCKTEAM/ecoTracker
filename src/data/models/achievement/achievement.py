from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.achievement.category import AchievementCategoryEnum
from src.core.enum.achievement.status import AchievementStatusEnum
from src.core.enum.language import LanguageEnum


class AchievementModel(Base):
    __tablename__ = "achievement"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[AchievementCategoryEnum]
    total: Mapped[int] = mapped_column(nullable=False)


class AchievementTranslateModel(Base):
    __tablename__ = "achievement_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievement.id"))
    language: Mapped[LanguageEnum]


class AchievementProgressModel(Base):
    __tablename__ = "achievement_progress"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievement.id"))
    entity_name: Mapped[str]
    entity_pointer: Mapped[str]
    counter: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(default=True)
    status: Mapped[AchievementStatusEnum]
