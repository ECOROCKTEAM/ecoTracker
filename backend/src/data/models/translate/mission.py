from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.application.database.holder import Base
from src.core.enum.language import LanguageEnum


class MissionTranslateModel(Base):
    __tablename__ = "mission_translate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    instruction: Mapped[str] = mapped_column()
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"))
    language: Mapped[LanguageEnum]
