from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.src.data.base.base_models import BaseUniquePrimaryKeyName


class ConstrainsVariableType(BaseUniquePrimaryKeyName):
    __tablename__ = "constrains_variable_type"


class Constrains(BaseUniquePrimaryKeyName):
    __tablename__ = "constrains"

    value: Mapped[str] = mapped_column(String)
    variable_type: Mapped[str] = mapped_column(ForeignKey(""))

    subscription_type_constrains: Mapped["SubscriptionTypeConstrains"] = relationship()


class SubscriptionTypeConstrains():
    name: Mapped[str] = mapped_column(ForeignKey("subscription_type.name"))
    contrains: Mapped[str] = mapped_column(ForeignKey("constrains.name"))


class SubscriptionType(BaseUniquePrimaryKeyName):
    __tablename__ = "subscription_type"


class SubscriptionPeriodUnit(BaseUniquePrimaryKeyName):
    __tablename__ = "subscription_period_unit"

    subscription_period: Mapped["SubscriptionPeriod"] = relationship()


class SubscriptionPeriod(BaseUniquePrimaryKeyName):
    __tablename__ = "subscription_period"

    value: Mapped[int] = mapped_column(Integer)
    unit: Mapped[str] = mapped_column(
        ForeignKey("subscription_period_unit.name"))

    subscriptions: Mapped["Subscription"] = relationship()


class Subscription(BaseUniquePrimaryKeyName):
    __tablename__ = "subscription"

    subscription_type_name: Mapped[str] = mapped_column(
        ForeignKey("subscription_type.name"))
    subscription_period: Mapped[str] = mapped_column(
        ForeignKey("subscription_period.name"))

    subscription_user: Mapped["SubscriptionUser"] = relationship()


class SubscriptionUser():
    __tablename__ = "subscription_user"

    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    canceled: Mapped[bool] = mapped_column(Boolean)
    until_date: Mapped[datetime] = mapped_column(DateTime)

    subscription_name: Mapped[str] = mapped_column(
        ForeignKey("subscription.name"))
