import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base


# read .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DB url not found in env varible")

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db():
    """
    Automatically create tables from Base.metadata if the database is empty.
    Useful for first-time container startup.
    """
    inspector = inspect(engine)
    # If no tables exist except possibly alembic_version, create them
    existing_tables = inspector.get_table_names()
    if not existing_tables or (existing_tables == ["alembic_version"]):
        print("DB is empty, creating tables from Base.metadata...")
        # import tables
        from app.DB import models
        Base.metadata.create_all(bind=engine)
    else:
        print("DB is already initialized.")

# get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()