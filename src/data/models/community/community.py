from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class CommunityModel(Base):
    __tablename__ = "community"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    privacy: Mapped[CommunityPrivacyEnum] = mapped_column()


class CommunityMissionModel(Base):
    __tablename__ = "community_mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_date: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    people_required: Mapped[int | None]
    people_max: Mapped[int | None]
    place: Mapped[str | None]
    comment: Mapped[str | None]
    community_id: Mapped[int] = mapped_column(ForeignKey("community.id"))
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    status: Mapped[OccupancyStatusEnum]


@dataclass
class CommunityScoreModel(Base):
    __tablename__ = "community_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community_id: Mapped[int] = mapped_column(ForeignKey("community.id"))
    operation: Mapped[ScoreOperationEnum] = mapped_column()
    value: Mapped[int] = mapped_column()


class CommunityInviteModel(Base):
    __tablename__ = "community_invite"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community_id: Mapped[int] = mapped_column(ForeignKey("community.id"))
    code: Mapped[str]
    expire_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))
