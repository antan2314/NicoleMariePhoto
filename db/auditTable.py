import enum

from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, validates

from db.base import Base

class AuditEvent(enum.Enum):
    ADMIN_CREATED = 'admin_created'
    PASSWORD_RESET = 'password_reset'
    ADMIN_DISABLED = 'admin_disabled'
    ADMIN_ENABLED = 'admin_enabled'
    LOGIN_FAILED = 'login_failed'
    LOGIN_SUCCESS = 'login_success'

class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admin.id"))
    admin_email: Mapped[str] = mapped_column(String(320))
    actor: Mapped[str] = mapped_column(String(50))
    source: Mapped[str] = mapped_column(String(200))
    event: Mapped[AuditEvent] = mapped_column(Enum(AuditEvent))
