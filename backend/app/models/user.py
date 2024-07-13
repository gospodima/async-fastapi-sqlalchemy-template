from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class UserDB(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(server_default="false")
    is_active: Mapped[bool] = mapped_column(server_default="true")
