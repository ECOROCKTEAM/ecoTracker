from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.group.role import GroupRoleEnum
from src.core.enum.language import LanguageEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.enum.user.contact import ContactTypeEnum


@dataclass
class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column(default=True)
    language: Mapped[LanguageEnum] = mapped_column()


class UserContactModel(Base):
    __tablename__ = "user_contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    value: Mapped[str]
    type: Mapped[ContactTypeEnum] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    is_favorite: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        UniqueConstraint("user_id", "value", "type", name="uq_user_contact_user_id_values_types"),
        Index(
            "ix_uq_user_id_is_favorite",
            "user_id",
            "is_favorite",
            unique=True,
            postgresql_where=(is_favorite.is_(True)),
        ),
    )


class UserSubscriptionModel(Base):
    __tablename__ = "user_subscription"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"))
    cancelled: Mapped[bool] = mapped_column(default=True)
    until_date: Mapped[datetime] = mapped_column(DateTime)


@dataclass
class UserGroupModel(Base):
    __tablename__ = "user_group"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), primary_key=True)
    role: Mapped[GroupRoleEnum] = mapped_column()


@dataclass
class UserScoreModel(Base):
    __tablename__ = "user_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    task_totaly_completed: Mapped[int] = mapped_column()
    mission_totaly_completed: Mapped[int] = mapped_column()
    operation: Mapped[ScoreOperationEnum] = mapped_column()
    value: Mapped[int] = mapped_column()
