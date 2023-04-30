from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.application.database.base import Base
from src.core.enum.language import LanguageEnum


@dataclass
class OccupancyCategoryModel(Base):
    __tablename__ = "occupancy_category"

    id: Mapped[int] = mapped_column(primary_key=True)


class OccupancyCategoryTranslateModel(Base):
    __tablename__ = "occupancy_category_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))
    language: Mapped[LanguageEnum]
