from datetime import datetime

from sqlalchemy import Text, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.data.base.base_models import BaseUniquePrimaryKeyName


class CommunityPrivacy(BaseUniquePrimaryKeyName):
    __tablename__ = "community_privacy"


class CommunityScore:
    __tablename__ = "community_score"

    value: Mapped[int] = mapped_column(Integer)
    community: Mapped[str] = mapped_column(ForeignKey("community.name"))
    operation: Mapped[str] = mapped_column(ForeignKey("score_operation.name"))


class CommunityRole(BaseUniquePrimaryKeyName):
    __tablename__ = "community_role"


class CommunityUser:
    __tablename__ = "community_user"

    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    community_name: Mapped[str] = mapped_column(ForeignKey("community_name"))
    role: Mapped[str] = mapped_column(ForeignKey("community_role.name"))


class CommunityMission:
    __tablename__ = "community_mission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    community_name: Mapped[str] = mapped_column(ForeignKey("community.name"))
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    meeting_date: Mapped[datetime] = mapped_column(DateTime)
    people_required: Mapped[int] = mapped_column(Integer)
    place: Mapped[str] = mapped_column(Text)
    comment: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(ForeignKey("BaseUniquePrimaryKeyName.name"))


class Community:
    __tablename__ = "community"

    description: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean)

    type: Mapped[str] = mapped_column(ForeignKey("community_privacy.name"))
    total_score: Mapped[int] = mapped_column(ForeignKey("community_score.value"))

    users = relationship('User')