from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.data.base.base_models import BaseUniquePrimaryKeyName
from backend.src.data.subscription.models import SubscriptionUser
from backend.src.data.community.models import Community


""" После настроек по подключению БД добавить к классам наследование """


class TranslateContactType:
    __tablename__ = "translate_contact_type"

    contact_type_id: Mapped[int] = mapped_column(ForeignKey("contact_type.id"))
    name: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(ForeignKey("language.name"))


class ContactType:
    __tablename__ = "contact_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


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


class UserMission:
    __tablename__ = "user_mission"
    
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    status: Mapped[bool] = mapped_column(ForeignKey("occupancy_status.name"))


class User():
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(25), primary_key=True, unique=True)
    password: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription: Mapped[str] = mapped_column(ForeignKey("subscription.name"))

    user_contacts: Mapped["UserContact"] = relationship()
    subscription_user: Mapped["SubscriptionUser"] = relationship()
    community: Mapped["Community"] = relationship()

