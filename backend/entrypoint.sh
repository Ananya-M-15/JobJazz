#!/bin/sh
set -e

# JobJazz Container Startup Script
# 1. Run database migrations using runtime DATABASE_URL
# 2. Start Uvicorn on Render's assigned $PORT with fallback to 8000

echo "==> [JobJazz] Running Alembic database migrations..."
alembic upgrade head
echo "==> [JobJazz] Alembic database migrations applied successfully."

# If arguments are passed, execute them (e.g. custom container command)
if [ $# -gt 0 ]; then
    echo "==> [JobJazz] Executing custom command: $@"
    exec "$@"
fi

# Fall back to 8000 if PORT is not set by hosting provider
PORT="${PORT:-8000}"
echo "==> [JobJazz] Starting Uvicorn production server on port ${PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}"
