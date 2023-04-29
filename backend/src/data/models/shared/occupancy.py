from dataclasses import dataclass
from sqlalchemy.orm import mapped_column, Mapped
from src.application.database.base import Base


@dataclass
class OccupancyTypeModel(Base):
    __tablename__ = "occupancy_type"

    id: Mapped[int] = mapped_column(primary_key=True)


class OccupancyStatusModel(Base):
    __tablename__ = "occupancy_status"

    id: Mapped[int] = mapped_column(primary_key=True)
