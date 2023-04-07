from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped


class TranslateMission:
    __tablename__ = "translate_mission"

    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    instruction: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(ForeignKey("language.name"))


class Mission:
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    author: Mapped[str] = mapped_column(String)
    score: Mapped[int] = mapped_column(Integer)
    occupancy_type: Mapped[int] = mapped_column(ForeignKey("occupancy_type.id"))
