#!/bin/sh
set -e

# 1. Check DB connection and Run Alembic migrations if necessary
python3 check_db.py

# 2. Start FastAPI server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug