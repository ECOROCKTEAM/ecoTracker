from sqlalchemy import String
from sqlalchemy import Mapped, mapped_column


class BaseUniquePrimaryKeyName:

    name: Mapped[str] = mapped_column(String(30), unique=True, primary_key=True)


class ScoreOperation(BaseUniquePrimaryKeyName):
    __tablename__ = "score_operation"


class WorkCategory(BaseUniquePrimaryKeyName):
    __tablename__ = "work_category"

    """
    У нас возможно будут общие категории между тасками, миссиями и ачивками. Можно сделать 1 модель на всех (WorkCategory)
    """