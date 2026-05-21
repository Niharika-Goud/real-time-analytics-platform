from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


# User model for authentication and platform access
class User(Base):

    __tablename__ = "users"

    # Primary key for each user
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    # Unique email used for login authentication
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    # Securely hashed password
    password_hash: Mapped[str] = mapped_column(
        String(500)
    )