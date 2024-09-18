from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.language import LanguageEnum


@dataclass
class MissionModel(Base):
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    active: Mapped[bool] = mapped_column()
    score: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey("occupancy_category.id"))


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


@dataclass
class UserMissionModel(Base):
    __tablename__ = "user_mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.id"),
    )
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    date_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_close: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    status: Mapped[OccupancyStatusEnum] = mapped_column()


@dataclass
class GroupMissionModel(Base):
    __tablename__ = "group_mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    author: Mapped[str] = mapped_column()
    meeting_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    people_required: Mapped[int | None] = mapped_column()
    people_max: Mapped[int | None] = mapped_column()
    place: Mapped[str | None] = mapped_column()
    comment: Mapped[str | None] = mapped_column()
    date_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_close: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    status: Mapped[OccupancyStatusEnum] = mapped_column()
