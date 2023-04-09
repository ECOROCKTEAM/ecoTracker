from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.database.holder import Base
from src.core.enum.language import LanguageEnum


class PrivacyTypeTranslateModel(Base):
    __tablename__ = "privacy_type_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    type_id: Mapped[int] = mapped_column(ForeignKey("privacy_type.id"))
    language: Mapped[LanguageEnum]
