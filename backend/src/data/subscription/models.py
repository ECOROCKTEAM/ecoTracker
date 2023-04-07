from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.src.data.base.base_models import BaseUniquePrimaryKeyName


class VariableType(BaseUniquePrimaryKeyName):
    __tablename__ = "variable_type"


class Constrains(BaseUniquePrimaryKeyName):
    __tablename__ = "constrains"

    value: Mapped[str] = mapped_column(String)
    variable_type: Mapped[str] = mapped_column(ForeignKey("variable_type.name"))

    subscription_type_constrains: Mapped["SubscriptionTypeConstrains"] = relationship()


class SubscriptionTypeConstrains():
    id: Mapped[int] = mapped_column
    name: Mapped[str] = mapped_column(ForeignKey("subscription_type.id"))
    contrains: Mapped[str] = mapped_column(ForeignKey("constrains.name"))


class SubscriptionType():
    __tablename__ = "subscription_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TranslateSubscriptionType:
    __tablename__ = "translate_subscription_type"

    subscription_type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(ForeignKey("language.name"))



class TranslateSubscriptionPeriodUnit:
    __tablename__ = "translate_subscription_period_unit"

    subscription_repiod_unit_id: Mapped[int] = mapped_column(ForeignKey("subscription_period_unit.id"))
    name: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(ForeignKey("language.name"))


class SubscriptionPeriodUnit:
    __tablename__ = "subscription_period_unit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TranslateSubscriptionPeriod:
    __tablename__ = "translate_subscription_period"

    subscription_period_id: Mapped[int] = mapped_column(ForeignKey("subscription_period.id"))
    name: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(ForeignKey("language.name"))


class SubscriptionPeriod:
    __tablename__ = "subscription_period"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    value: Mapped[int] = mapped_column(Integer)
    unit: Mapped[str] = mapped_column(ForeignKey("subscription_period_unit.id"))

    subscriptions: Mapped["Subscription"] = relationship()


class TranslateSubscription:
    __tablename__ = "translate_subscription"

    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(ForeignKey("language.name"))


class Subscription(BaseUniquePrimaryKeyName):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subscription_type: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"))
    subscription_period: Mapped[str] = mapped_column(ForeignKey("subscription_period.id"))


class SubscriptionUser():
    __tablename__ = "subscription_user"

    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    subscription_name: Mapped[str] = mapped_column(ForeignKey("subscription.name"))
    canceled: Mapped[bool] = mapped_column(Boolean)
    until_date: Mapped[datetime] = mapped_column(DateTime)
    
