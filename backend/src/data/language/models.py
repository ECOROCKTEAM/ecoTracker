from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Language:
    __tablename__ = "language"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    code: Mapped[str] = mapped_column(String)
