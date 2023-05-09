from dataclasses import dataclass
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.application.database.base import Base
from src.core.enum.language import LanguageEnum

if TYPE_CHECKING:
    from src.data.models.challenges.occupancy import OccupancyCategoryModel


@dataclass
class MissionModel(Base):
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    active: Mapped[bool] = mapped_column()
    author: Mapped[str] = mapped_column()
    score: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))

    category: Mapped["OccupancyCategoryModel"] = relationship(lazy="joined", back_populates="missions")
    translations: Mapped[list["MissionTranslateModel"]] = relationship(lazy="selectin", back_populates="mission")


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

    mission: Mapped["MissionModel"] = relationship(lazy="noload", back_populates="translations")
