from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.enum.score import ScoreOPerationEnum

from src.application.database.holder import Base


class UserModel(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(primary_key=True, unique=True)
    password: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)

    contacts = relationship(
        "ContactModel",
        back_populates="user",
    )
    # role


class UserRoleApplicationModel(Base):
    __tablename__ = "user_role_application"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    role: Mapped[str] = mapped_column(ForeignKey("role_application.name"))


class RoleApplicationModel(Base):
    __tablename__ = "role_application"

    role: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)


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
    role_id: Mapped[str] = mapped_column(ForeignKey("community_role.id"))


class UserScoreModel(Base):
    __tablename__ = "user_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    operation: Mapped[ScoreOPerationEnum]
    value: Mapped[int]


class UserTaskModel(Base):
    __tablename__ = "user_task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    status_id: Mapped[str] = mapped_column(ForeignKey("occupancy_status.id"))


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
    status_id: Mapped[bool] = mapped_column(ForeignKey("occupancy_status.id"))
