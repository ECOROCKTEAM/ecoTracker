from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.database.holder import Base
from src.core.enum.base import VariableTypeEnum


class ValueTypeModel(Base):
    __tablename__ = "value_type"

    name: Mapped[str] = mapped_column(primary_key=True, unique=True)


class ConstraintModel(Base):
    __tablename__ = "constraint"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    value: Mapped[str] = mapped_column()
    value_type: Mapped[VariableTypeEnum]


class PrivacyTypeModel(Base):
    __tablename__ = "privacy_type"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
