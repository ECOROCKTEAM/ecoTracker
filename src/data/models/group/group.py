from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class GroupModel(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    privacy: Mapped[GroupPrivacyEnum] = mapped_column()
    code: Mapped[str | None] = mapped_column(unique=True)
    code_expire_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))


@dataclass
class GroupScoreModel(Base):
    __tablename__ = "group_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    operation: Mapped[ScoreOperationEnum] = mapped_column()
    value: Mapped[int] = mapped_column()
    mission_totaly_completed: Mapped[int] = mapped_column()
