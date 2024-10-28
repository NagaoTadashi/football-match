#!/bin/sh
# entrypoint.sh

# Run database migrations
alembic upgrade head

# Start FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8080
