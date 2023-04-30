from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.application.database.base import Base
from src.core.enum.language import LanguageEnum


class MissionModel(Base):
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    active: Mapped[bool]
    author: Mapped[str]
    score: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))


class MissionTranslateModel(Base):
    __tablename__ = "mission_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    instruction: Mapped[str]
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    language: Mapped[LanguageEnum]
