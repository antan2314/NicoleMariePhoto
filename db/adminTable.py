from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, validates
from base import Base

class Admin(Base):
    __tablename__ = 'admin'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    password_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    disabled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


    @validates("email")
    def validate_email(self, key, address):
        stripped_address = address.strip()
        lowered_address = stripped_address.lower()
        if "@" not in lowered_address:
            raise ValueError("Failed simple email validation")
        return lowered_address