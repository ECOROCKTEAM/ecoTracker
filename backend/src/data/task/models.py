from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped


class Task:
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    score: Mapped[int] = mapped_column(Integer)
    occupancy_id: Mapped[int] = mapped_column(ForeignKey("occupancy_type.id"))


class UserTask:
    __tablename__ = "user_task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(ForeignKey("user.username"))
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    status: Mapped[str] = mapped_column(ForeignKey("occupancy_status.name"))