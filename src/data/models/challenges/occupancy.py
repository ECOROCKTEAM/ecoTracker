from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.database.base import Base
from src.core.enum.language import LanguageEnum

if TYPE_CHECKING:
    from src.data.models.challenges.mission import MissionModel


@dataclass
class OccupancyCategoryModel(Base):
    __tablename__ = "occupancy_category"

    id: Mapped[int] = mapped_column(primary_key=True)

    translations: Mapped[list["OccupancyCategoryTranslateModel"]] = relationship(
        lazy="selectin", back_populates="category"
    )
    missions: Mapped[list["MissionModel"]] = relationship(lazy="noload", back_populates="category")


@dataclass
class OccupancyCategoryTranslateModel(Base):
    __tablename__ = "occupancy_category_translate"
    __table_args__ = (
        UniqueConstraint(
            "category_id",
            "language",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))
    language: Mapped[LanguageEnum] = mapped_column()

    category: Mapped["OccupancyCategoryModel"] = relationship(lazy="noload", back_populates="translations")
