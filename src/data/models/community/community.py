from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.enum.score.operation import ScoreOperationEnum


class CommunityModel(Base):
    __tablename__ = "community"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)
    privacy: Mapped[CommunityPrivacyEnum]


@dataclass
class CommunityMissionModel(Base):
    __tablename__ = "community_mission"

    community_id: Mapped[int] = mapped_column(ForeignKey("community.id"), primary_key=True, autoincrement=False)
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"), primary_key=True, autoincrement=False)
    author: Mapped[str] = mapped_column()
    meeting_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))
    people_required: Mapped[int | None] = mapped_column()
    people_max: Mapped[int | None] = mapped_column()
    place: Mapped[str | None] = mapped_column()
    comment: Mapped[str | None] = mapped_column()
    date_close: Mapped[datetime | None] = mapped_column(default=None)
    status: Mapped[OccupancyStatusEnum] = mapped_column()


class CommunityScoreModel(Base):
    __tablename__ = "community_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community_id: Mapped[int] = mapped_column(ForeignKey("community.id"))
    operation: Mapped[ScoreOperationEnum]
    value: Mapped[int]


class CommunityInviteModel(Base):
    __tablename__ = "community_invite"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community_id: Mapped[int] = mapped_column(ForeignKey("community.id"))
    code: Mapped[str]
    expire_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))
