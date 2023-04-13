from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.enum.score import ScoreOPerationEnum
from src.application.database.holder import Base


class CommunityModel(Base):
    __tablename__ = "community"

    name: Mapped[str] = mapped_column(primary_key=True, unique=True)
    description: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    privacy_type_id: Mapped[int] = mapped_column(ForeignKey("privacy_type.id"))


class CommunityRoleModel(Base):
    __tablename__ = "community_role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class CommunityMissionModel(Base):
    __tablename__ = "community_mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meeting_date: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    people_required: Mapped[Optional[int]]
    people_max: Mapped[Optional[int]]
    place: Mapped[Optional[str]]
    comment: Mapped[Optional[str]]
    community: Mapped[str] = mapped_column(ForeignKey("community.name"))
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    status_id: Mapped[bool] = mapped_column(ForeignKey("occupancy_status.id"))


class CommunityScoreModel(Base):
    __tablename__ = "community_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community: Mapped[str] = mapped_column(ForeignKey("community.name"))
    operation: Mapped[ScoreOPerationEnum]
    value: Mapped[int]


class CommunityInviteModel(Base):
    __tablename__ = "community_invite"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    community: Mapped[str] = mapped_column(ForeignKey("community.name"))
    code: Mapped[str]
    expire_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))