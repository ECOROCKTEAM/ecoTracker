from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.data.subscription.models import Subscription


""" После настроек по подключению БД добавить к классам наследование """


class User():
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(25), primary_key=True, unique=True)
    password: Mapped[str] = mapped_column(String(30))
    active: Mapped[bool] = mapped_column(Boolean, default=False)

    subscription: Mapped["Subscription"] = relationship("username")