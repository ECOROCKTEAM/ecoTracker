from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.application.database.holder import Base


class TaskModel(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    score: Mapped[int] = mapped_column()
    occupancy_id: Mapped[int] = mapped_column(ForeignKey("occupancy_type.id"))
