from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.base import Base
from src.core.enum.language import LanguageEnum


class ContactTypeTranslateModel(Base):
    __tablename__ = "contact_type_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("contact_type.id"))
    language: Mapped[LanguageEnum]
