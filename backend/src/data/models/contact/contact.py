from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.application.database.holder import Base


class ContactModel(Base):
    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("contact_type.id"))

    type = relationship(
        "ContactTypeModel",
        back_populates="contacts",
        uselist=False,
    )
    user = relationship(
        "UserModel", secondary="user_contact", back_populates="contacts"
    )


class ContactTypeModel(Base):
    __tablename__ = "contact_type"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    contacts = relationship("ContactTypeModel", back_populates="type", uselist=True)
