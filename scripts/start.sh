#!/usr/bin/env bash
# Start the FastAPI server with auto-reload.
# Assumes setup.sh has already been run.
#
# Usage: ./scripts/start.sh

set -euo pipefail
cd "$(dirname "$0")/.."

# Make sure the DB container is up (no-op if already running).
docker compose up -d db

echo "▸ Starting API at http://localhost:8000"
echo "  Swagger UI: http://localhost:8000/docs"
echo
exec uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
