from sqlalchemy import String
from sqlalchemy import Mapped, mapped_column


class BaseUniquePrimaryKeyName:

    name: Mapped[str] = mapped_column(String(30), unique=True, primary_key=True)



class ScoreOperation(BaseUniquePrimaryKeyName):
    __tablename__ = "score_operation"