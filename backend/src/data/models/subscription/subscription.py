from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.holder import Base


class SubscriptionModel(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"))
    period_id: Mapped[int] = mapped_column(ForeignKey("subscription_period.id"))


class SubscriptionTypeModel(Base):
    __tablename__ = "subscription_type"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class SubscriptionTypeConstraintModel(Base):
    __tablename__ = "subscription_type_constraint"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"))
    constraint_id: Mapped[int] = mapped_column(ForeignKey("constraint.id"))


class SubscriptionPeriodModel(Base):
    __tablename__ = "subscription_period"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column()
    unit_id: Mapped[int] = mapped_column(ForeignKey("subscription_period_unit.id"))


class SubscriptionPeriodUnitModel(Base):
    __tablename__ = "subscription_period_unit"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
