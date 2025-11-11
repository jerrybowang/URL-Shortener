import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.DB.database import init_db, Base

from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata


# Load .env
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DB url not found in env variable")

engine = create_engine(DATABASE_URL)

# wait for DB to be ready
for i in range(30):  # try up to 30 times (~30s)
    try:
        with engine.connect():
            print("Database is ready")
            break
    except OperationalError:
        print("Waiting for DB...")
        time.sleep(1)
else:
    raise RuntimeError("Could not connect to the database after 30 seconds")


init_db()

# check for model changes
with engine.connect() as conn:
    ctx = MigrationContext.configure(conn)
    # import tables
    # use "noqa: F401" for ruff to ignore import error for this line
    from app.DB import models  # noqa: F401

    diff = compare_metadata(ctx, Base.metadata)

    if diff:
        print("Model changes detected, generating migration...")
        # Run alembic revision + upgrade programmatically
        from alembic.config import Config
        from alembic import command

        alembic_cfg = Config("alembic.ini")
        command.revision(
            alembic_cfg, message="auto sync with DB models", autogenerate=True
        )
        command.upgrade(alembic_cfg, "head")
    else:
        print("No model changes detected, skipping migration.")
