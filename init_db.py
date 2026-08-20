from db.base import Base
from db.adminTable import Admin
from db.auditTable import AuditLog

from sqlalchemy import create_engine

engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)

