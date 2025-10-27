import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.DB.database import init_db

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