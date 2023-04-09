from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped
from src.application.database.holder import Base


class AchievementModel(Base):
    __tablename__ = "achievement"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("achievement_category.id"), nullable=False
    )
    total: Mapped[int] = mapped_column(nullable=False)


class AchievementCategoryModel(Base):
    __tablename__ = "achievement_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class AchievementProgressModel(Base):
    __tablename__ = "achievement_progress"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievement.id"))
    entity_name: Mapped[str] = mapped_column()
    entity_pointer: Mapped[str] = mapped_column()
    counter: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(default=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("achievement_progress_status.id"))


class AchievementProgressStatusModel(Base):
    __tablename__ = "achievement_progress_status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
