from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.holder import Base
from src.core.enum.application.language import LanguageEnum


class SubscriptionTranslateModel(Base):
    __tablename__ = "subscription_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"))
    language: Mapped[LanguageEnum]


class SubscriptionTypeTranslateModel(Base):
    __tablename__ = "subscription_type_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"))
    language: Mapped[LanguageEnum]


class SubscriptionPeriodTranslateModel(Base):
    __tablename__ = "subscription_period_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("subscription_period.id"))
    language: Mapped[LanguageEnum]


class SubscriptionPeriodUnitTranslateModel(Base):
    __tablename__ = "subscription_period_unit_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("subscription_period_unit.id"))
    language: Mapped[LanguageEnum]


class CommunityRoleTranslateModel(Base):
    __tablename__ = "community_role_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("community_role.id"))
    language: Mapped[LanguageEnum]
