from typing import List

from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.data.subscription.models import SubscriptionUser
from backend.src.data.mission.models import Mission
from backend.src.data.community.models import Community
from backend.src.data.language.models import Language


""" После настроек по подключению БД добавить к классам наследование """


class TranslateContactType:
    __tablename__ = "translate_contact_type"

    contact_type_id: Mapped[int] = mapped_column(ForeignKey("contact_type.id"))
    name: Mapped[str] = mapped_column(String)
    language: Mapped[str] = mapped_column(ForeignKey("language.name"))


class ContactType:
    __tablename__ = "contact_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    language_name: Mapped[str] = mapped_column(ForeignKey("language.name"))
    language: Mapped['Language'] = relationship(foreign_keys=[language_name])


class Contact:
    __tablename__ = "contact"

    value: Mapped[str] = mapped_column(String, unique=True)
    contact_type: Mapped[str] = mapped_column(ForeignKey("contact_type.name"))

    user_contact: Mapped['UserContact'] = relationship(back_populates="contacts")


class UserContact:
    __tablename__ = "user_contact"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    contact: Mapped[str] = mapped_column(ForeignKey("contact.value"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    contacts: Mapped["Contact"] = relationship(back_populates="user_contact")
    user: Mapped["User"] = relationship(back_populates="contacts")


class UserMission:
    __tablename__ = "user_mission"
    
    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    status: Mapped[bool] = mapped_column(ForeignKey("occupancy_status.name"))

    mission: Mapped['Mission'] = relationship()
    users: Mapped[List['User']] = relationship(back_populates="user_missions")


class User:
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(25), primary_key=True, unique=True)
    password: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column(Boolean, default=False)

    subscription_user: Mapped['SubscriptionUser'] = relationship(back_populates="users")
    user_missions: Mapped[List['UserMission']] = relationship(back_populates="users")
    contacts: Mapped[List['UserContact']] = relationship(back_populates="user")
    communityes: Mapped[List['Community']] = relationship(back_populates="users", secondary="community_user")
