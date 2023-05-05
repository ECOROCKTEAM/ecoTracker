from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.enum.community.role import CommunityRoleEnum
from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass  # TODO remove
class UserModel(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(primary_key=True, unique=True)
    password: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)

    # contacts = relationship(
    #     "ContactModel",
    #     back_populates="user",
    # )
    # role


class UserContactModel(Base):
    __tablename__ = "user_contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    contact_id: Mapped[str] = mapped_column(ForeignKey("contact.id"), unique=True)
    active: Mapped[bool] = mapped_column(default=True)


class UserSubscriptionModel(Base):
    __tablename__ = "user_subscription"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"))
    cancelled: Mapped[bool] = mapped_column(default=True)
    until_date: Mapped[datetime] = mapped_column(DateTime)


class UserCommunityModel(Base):
    __tablename__ = "user_community"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    community_name: Mapped[str] = mapped_column(ForeignKey("community.name"))
    role: Mapped[CommunityRoleEnum]


class UserScoreModel(Base):
    __tablename__ = "user_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    operation: Mapped[ScoreOperationEnum]
    value: Mapped[int]


class UserTaskModel(Base):
    __tablename__ = "user_task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    status: Mapped[OccupancyStatusEnum]


class UserMissionModel(Base):
    __tablename__ = "user_mission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        ForeignKey("user.username"),
        nullable=False,
        primary_key=True,
        autoincrement=False,
    )
    mission_id: Mapped[int] = mapped_column(
        ForeignKey("mission.id"), nullable=False, primary_key=True, autoincrement=False
    )
    status: Mapped[OccupancyStatusEnum]
