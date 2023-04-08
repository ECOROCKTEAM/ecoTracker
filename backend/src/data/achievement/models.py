from typing import List

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm  import Mapped, mapped_column, relationship

from application.database.holder import Base


class AchievementProgress:
    __tablename__ = "achievement_progress"

    name: Mapped[str] = mapped_column(ForeignKey("achievement.name"), nullable=False, primary_key=True)
    point_counter: Mapped[int] = mapped_column(nullable=False, default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    entity_name: Mapped[str] = mapped_column(nullable=False)
    entity_id: Mapped[int] = mapped_column(nullable=False)


class AchievementType(Base):
    __tablename__ = "achievement_type"
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    
    achievements: Mapped[List["Achievement"]] = relationship(back_populates="type")

class Achievement:
    __tablename__ = "achievement"

    name: Mapped[str] = mapped_column(unique=True, primary_key=True)
    type_id: Mapped[str] = mapped_column(ForeignKey("achievement_type.id"), nullable=False)
    total: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    
    type: Mapped["AchievementType"] = relationship(back_populates="achievements", lazy="joined")
