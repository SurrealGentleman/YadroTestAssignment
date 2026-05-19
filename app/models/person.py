from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gender: Mapped[str] = mapped_column(default="", index=True)
    first_name: Mapped[str] = mapped_column(default="", index=True)
    last_name: Mapped[str] = mapped_column(default="", index=True)
    phone: Mapped[str] = mapped_column(default="")
    email: Mapped[str] = mapped_column(default="", index=True)
    address: Mapped[str] = mapped_column(Text, default="")
    raw_data: Mapped[str] = mapped_column(Text, default="{}")

