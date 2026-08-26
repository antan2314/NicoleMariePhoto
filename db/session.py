from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Resolve the database location relative to this file rather than the current
# working directory, so the same app.db is used no matter where a script is
# launched from. session.py lives in db/, so the project root is two levels up.
session_path = Path(__file__).resolve()
project_root_path = session_path.parent.parent
db_path = project_root_path / "app.db"

# Single engine for the process; it owns the connection pool to the SQLite file.
engine = create_engine(f"sqlite:///{db_path}")

# Session factory bound to that engine. Call Session() to get a new session
# per unit of work rather than sharing one session across the whole program.
Session = sessionmaker(bind=engine)
