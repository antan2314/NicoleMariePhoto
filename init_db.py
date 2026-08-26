from db.base import Base

# The table classes must be imported before create_all() runs: importing them
# is what registers each model on Base.metadata. They look unused here, but
# removing these imports would leave metadata empty and create no tables.
from db.adminTable import Admin
from db.auditTable import AuditLog
from db.session import engine


# Creates any tables that don't exist yet. Existing tables are left untouched,
# so this is safe to re-run, but it will not migrate tables whose columns have
# since changed - those need to be dropped or migrated by hand.
Base.metadata.create_all(engine)
