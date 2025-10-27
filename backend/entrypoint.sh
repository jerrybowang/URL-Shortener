#!/bin/sh
set -e

# 1. Check DB connection
python3 check_db.py

# 2. Run Alembic migrations
alembic upgrade head

# 3. Start FastAPI server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug