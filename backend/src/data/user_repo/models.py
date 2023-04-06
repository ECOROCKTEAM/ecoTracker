from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.data.base.base_models import BaseUniquePrimaryKeyName
from backend.src.data.subscription.models import SubscriptionUser
from backend.src.data.community.models import Community


""" После настроек по подключению БД добавить к классам наследование """


class ContactType(BaseUniquePrimaryKeyName):
    __tablename__ = "contact_type"


class Contact:
    __tablename__ = "contact"

    value: Mapped[str] = mapped_column(String, unique=True)
    contact_type: Mapped[str] = mapped_column(ForeignKey("contact_type.name"))


class UserContact:
    __tablename__ = "user_contact"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    contact: Mapped[str] = mapped_column(ForeignKey("contact.value"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    contacts: Mapped["Contact"] = relationship()
    users: Mapped["User"] = relationship()


class User():
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(25), primary_key=True, unique=True)
    password: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription: Mapped[str] = mapped_column(ForeignKey("subscription.name"))

    user_contacts: Mapped["UserContact"] = relationship()
    subscription_user: Mapped["SubscriptionUser"] = relationship()
    community: Mapped["Community"] = relationship()