from dataclasses import dataclass

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.language import LanguageEnum


@dataclass
class MissionModel(Base):
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    active: Mapped[bool] = mapped_column()
    author: Mapped[str] = mapped_column()
    score: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))


@dataclass
class MissionTranslateModel(Base):
    __tablename__ = "mission_translate"
    __table_args__ = (
        UniqueConstraint(
            "mission_id",
            "language",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    instruction: Mapped[str] = mapped_column()
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    language: Mapped[LanguageEnum] = mapped_column()
