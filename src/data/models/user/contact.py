from sqlalchemy.orm import Mapped, mapped_column
from src.application.database.base import Base
from src.core.enum.user.contact import ContactTypeEnum


class ContactModel(Base):
    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[str]
    type: Mapped[ContactTypeEnum]

    # type = relationship(
    #     "ContactTypeModel",
    #     back_populates="contacts",
    #     uselist=False,
    # )
    # user = relationship("UserModel", secondary="user_contact", back_populates="contacts")
