from base import Base
from adminTable import Admin
from auditTable import AuditLog

from sqlalchemy import create_engine

engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)

