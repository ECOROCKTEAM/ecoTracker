from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.enum.challenges.status import OccupancyStatusEnum


class CommunityModel(Base):
    __tablename__ = "community"

    name: Mapped[str] = mapped_column(primary_key=True, unique=True)
    description: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)
    privacy: Mapped[CommunityPrivacyEnum]


class CommunityMissionModel(Base):
    __tablename__ = "community_mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_date: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    people_required: Mapped[int | None]
    people_max: Mapped[int | None]
    place: Mapped[str | None]
    comment: Mapped[str | None]
    community: Mapped[str] = mapped_column(ForeignKey("community.name"))
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    status: Mapped[OccupancyStatusEnum]


class CommunityScoreModel(Base):
    __tablename__ = "community_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community: Mapped[str] = mapped_column(ForeignKey("community.name"))
    operation: Mapped[ScoreOperationEnum]
    value: Mapped[int]


class CommunityInviteModel(Base):
    __tablename__ = "community_invite"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community: Mapped[str] = mapped_column(ForeignKey("community.name"))
    code: Mapped[str]
    expire_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))
