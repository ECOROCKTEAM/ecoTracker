from dataclasses import dataclass

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.language import LanguageEnum


@dataclass
class OccupancyCategoryModel(Base):
    __tablename__ = "occupancy_category"

    id: Mapped[int] = mapped_column(primary_key=True)


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
