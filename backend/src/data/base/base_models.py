from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.language.models import Language


class BaseUniquePrimaryKeyName:

    name: Mapped[str] = mapped_column(String(30), unique=True, primary_key=True)


class ScoreOperation(BaseUniquePrimaryKeyName):
    __tablename__ = "score_operation"


class TranslateOccupancyType:
    __tablename__ = 'translate_occupancy_type'

    occupancy_type_id: Mapped[int] = mapped_column(ForeignKey("occupancy_type.id"))
    name: Mapped[str] = mapped_column(String)
    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])


class OccupancyType:
    __tablename__ = "occupancy_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    translate: Mapped['TranslateOccupancyType'] = relationship()



class TranslateOccupancyStatus:
    __tablename__ = 'translate_occupancy_status'

    occupancy_status_id: Mapped[int] = mapped_column(ForeignKey("occupancy_status.id"))
    name: Mapped[str] = mapped_column(String)
    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])


class OccupancyStatus:
    __tablename__ = "occupancy_status"

    id: Mapped[int] = mapped_column(Integer, primary_key= True)

    