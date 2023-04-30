from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.language import LanguageEnum
from src.core.enum.subscription.subscription import (
    SubscriptionPeriodUnitEnum,
    SubscriptionTypeEnum,
)


class SubscriptionModel(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[SubscriptionTypeEnum]
    period_id: Mapped[int] = mapped_column(ForeignKey("subscription_period.id"))


class SubscriptionTranslateModel(Base):
    __tablename__ = "subscription_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"))
    language: Mapped[LanguageEnum]


class SubscriptionPeriodModel(Base):
    __tablename__ = "subscription_period"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[str]
    unit: Mapped[SubscriptionPeriodUnitEnum]
