from sqlalchemy import ForeignKey, Integer, Boolean, Text, String
from sqlalchemy.orm  import Mapped, mapped_column

from backend.src.data.base.base_models import BaseUniquePrimaryKeyName

"""
    У нас возможно будут общие категории между тасками, миссиями и ачивками. Можно сделать 1 модель на всех (WorkCategory)
"""


class AchievementProgress:
    __tablename__ = "achievement_progress"

    name: Mapped[str] = mapped_column(ForeignKey("achievement.name"))
    point_counter: Mapped[int] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    entity_name: Mapped[str] = mapped_column(String)
    entity_id: Mapped[int] = mapped_column(Integer)



class Achievement(BaseUniquePrimaryKeyName):
    __tablename__ = "achievement"

    category: Mapped[str] = mapped_column(ForeignKey("work_category.name"))
    total: Mapped[int] = mapped_column(Integer)
    status: Mapped[bool] = mapped_column(Boolean)
    description: Mapped[str] = mapped_column(Text)
