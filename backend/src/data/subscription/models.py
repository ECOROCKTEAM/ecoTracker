from typing import List

from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.src.data.base.base_models import BaseUniquePrimaryKeyName
from backend.src.data.user_repo.models import User
from backend.src.data.language.models import Language


class VariableType(BaseUniquePrimaryKeyName):
    __tablename__ = "variable_type"

    constrain: Mapped[List['Constrains']] = relationship()


class Constrains(BaseUniquePrimaryKeyName):
    __tablename__ = "constrains"

    value: Mapped[str] = mapped_column(String)
    variable_type: Mapped[str] = mapped_column(ForeignKey("variable_type.name"))

    subscription_type_constrains: Mapped["SubscriptionType"] = relationship(secondary="subscription_type_constrains")


class SubscriptionTypeConstrains():
    __tablename__ = "subscription_type_constrains"

    id: Mapped[int] = mapped_column
    name: Mapped[str] = mapped_column(ForeignKey("subscription_type.id"))
    contrains: Mapped[str] = mapped_column(ForeignKey("constrains.name"))


class SubscriptionType():
    __tablename__ = "subscription_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    translate: Mapped['TranslateSubscriptionType'] = relationship()
    constrains: Mapped['Constrains'] = relationship(secondary="subscription_type_constrains")
    subscription: Mapped['Subscription'] = relationship(back_populates="subscription_type")


class TranslateSubscriptionType:
    __tablename__ = "translate_subscription_type"

    subscription_type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])



class TranslateSubscriptionPeriodUnit:
    __tablename__ = "translate_subscription_period_unit"

    subscription_repiod_unit_id: Mapped[int] = mapped_column(ForeignKey("subscription_period_unit.id"))
    name: Mapped[str] = mapped_column(String)
    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])


class SubscriptionPeriodUnit:
    __tablename__ = "subscription_period_unit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    translate: Mapped['TranslateSubscriptionPeriodUnit'] = relationship()
    subscription_period: Mapped['SubscriptionPeriod'] = relationship(back_populates="subscription_period_unit")


class TranslateSubscriptionPeriod:
    __tablename__ = "translate_subscription_period"

    subscription_period_id: Mapped[int] = mapped_column(ForeignKey("subscription_period.id"))
    name: Mapped[str] = mapped_column(String)
    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])


class SubscriptionPeriod:
    __tablename__ = "subscription_period"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    value: Mapped[int] = mapped_column(Integer)
    unit: Mapped[str] = mapped_column(ForeignKey("subscription_period_unit.id"))

    translate: Mapped['TranslateSubscriptionPeriod'] = relationship()
    subscription_period_unit: Mapped['SubscriptionPeriodUnit'] = relationship(back_populates="subscription_period")
    subscription: Mapped["Subscription"] = relationship(back_populates="subscription_period")


class TranslateSubscription:
    __tablename__ = "translate_subscription"

    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])


class Subscription:
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subscription_type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"))
    subscription_period_id: Mapped[str] = mapped_column(ForeignKey("subscription_period.id"))

    subscription_type: Mapped['SubscriptionType'] = relationship(back_populates="subscription")
    subscription_period: Mapped['SubscriptionPeriod'] = relationship(back_populates="subscriptions")


class SubscriptionUser():
    __tablename__ = "subscription_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    subscription_name: Mapped[str] = mapped_column(ForeignKey("subscription.name"))
    canceled: Mapped[bool] = mapped_column(Boolean)
    until_date: Mapped[datetime] = mapped_column(DateTime)
    
    users: Mapped[List['User']] = relationship(back_populates="subscription_user")