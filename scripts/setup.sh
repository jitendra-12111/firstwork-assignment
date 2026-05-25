#!/usr/bin/env bash
# One-shot project bootstrap. Idempotent — safe to re-run.
#
# Steps:
#   1. uv venv + sync (creates .venv, installs deps from uv.lock)
#   2. docker compose up -d db (start MySQL)
#   3. Wait for DB healthcheck
#   4. alembic upgrade head (run migrations)
#   5. Load docs/seed.sql (idempotent — TRUNCATEs first)
#
# Usage: ./scripts/setup.sh

set -euo pipefail

cd "$(dirname "$0")/.."   # always run from project root

echo "▸ 1/5  Creating venv + installing dependencies"
uv sync

echo "▸ 2/5  Starting MySQL container"
docker compose up -d db

echo "▸ 3/5  Waiting for MySQL to be healthy"
until [ "$(docker inspect -f '{{.State.Health.Status}}' firstwork_db 2>/dev/null)" = "healthy" ]; do
  printf "."
  sleep 2
done
echo " ready"

echo "▸ 4/5  Running migrations"
uv run alembic upgrade head

echo "▸ 5/5  Loading seed data"
docker compose exec -T db mysql -u root -psecret firstwork < docs/seed.sql

echo
echo "✓ Setup complete."
echo "  Start server: ./scripts/start.sh"
echo "  Run tests:    ./scripts/test.sh"
