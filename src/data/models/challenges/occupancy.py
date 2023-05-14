from dataclasses import dataclass
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.application.database.base import Base
from src.core.enum.language import LanguageEnum

if TYPE_CHECKING:
    from src.data.models.challenges.task import TaskModel


@dataclass
class OccupancyCategoryModel(Base):
    __tablename__ = "occupancy_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    translations: Mapped[list["OccupancyCategoryTranslateModel"]] = relationship(
        lazy="selectin", back_populates="category"
    )

    tasks: Mapped[list["TaskModel"]] = relationship(lazy="noload", back_populates="category")


class OccupancyCategoryTranslateModel(Base):
    __tablename__ = "occupancy_category_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))
    language: Mapped[LanguageEnum]

    category: Mapped["OccupancyCategoryModel"] = relationship(lazy="noload", back_populates="translations")
