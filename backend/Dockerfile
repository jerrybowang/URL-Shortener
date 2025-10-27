# --- Backend Dockerfile ---
FROM python:3.14-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY ./app ./app

# Copy DB migration script
COPY ./alembic /app/alembic/
COPY ./alembic.ini /app/

# Copy start up script
COPY ./check_db.py /app/
COPY ./entrypoint.sh /app/

# For hot reload during development, we’ll override this CMD in docker-compose
CMD ["/bin/sh", "/app/entrypoint.sh"]
