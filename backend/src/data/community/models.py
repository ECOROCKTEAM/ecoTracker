from datetime import datetime
from typing import List

from sqlalchemy import Text, Boolean, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.user_repo.models import User
from src.data.mission.models import Mission
from src.data.language.models import Language


class TranslateCommunityPrivacy:
    __tablename__ = "translate_community_privacy"
    
    community_privacy_id: Mapped[int] = mapped_column(ForeignKey("community_privacy.id"))
    name: Mapped[str] = mapped_column(String)

    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])


class CommunityPrivacy():
    __tablename__ = "community_privacy"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    translate: Mapped['TranslateCommunityPrivacy'] = relationship()


class CommunityScore:
    __tablename__ = "community_score"

    value: Mapped[int] = mapped_column(Integer)
    community: Mapped[str] = mapped_column(ForeignKey("community.name"))
    operation: Mapped[str] = mapped_column(ForeignKey("score_operation.name"))


class TranslateCommunityRole:
    __tablename__ = "translate_community_role"

    community_role_id: Mapped[int] = mapped_column(ForeignKey("community_role.id"))
    name: Mapped[str] = mapped_column(String)
    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])



class CommunityRole:
    __tablename__ = "community_role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    translate: Mapped['TranslateCommunityRole'] = relationship()


class CommunityUser:
    __tablename__ = "community_user"

    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    community_name: Mapped[str] = mapped_column(ForeignKey("community_name"))
    role_id: Mapped[int] = mapped_column(ForeignKey("community_role.id"))

    community_role: Mapped['CommunityRole'] = relationship("CommunityRole", foreign_keys=[role_id])


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

    mission: Mapped['Mission'] = relationship()


class Community:
    __tablename__ = "community"

    description: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean)

    type: Mapped[str] = mapped_column(ForeignKey("community_privacy.id"))
    total_score: Mapped[int] = mapped_column(ForeignKey("community_score.value"))

    community_missions: Mapped[List["CommunityMission"]] = relationship()
    
    # users: Mapped[List["User"]] = relationship(secondary="community_user", back_populates="communityes")
    users = relationship('User')