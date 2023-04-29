from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.application.database.base import Base
from src.core.enum.application.language import LanguageEnum


class OccupancyTypeTranslateModel(Base):
    __tablename__ = "occupancy_type_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("occupancy_type.id"))
    language: Mapped[LanguageEnum]


class OccupancyStatusTranslateModel(Base):
    __tablename__ = "occupancy_status_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    status_id: Mapped[int] = mapped_column(ForeignKey("occupancy_status.id"))
    language: Mapped[LanguageEnum]
