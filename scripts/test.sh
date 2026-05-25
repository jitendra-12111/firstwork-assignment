#!/usr/bin/env bash
# Run the pytest suite across all test folders.
#
# Tests use FastAPI's TestClient (in-process) — no need to start the server.
# But MySQL must be up and seeded (run `make setup` first if you haven't).
#
# Usage:
#   ./scripts/test.sh                    # all tests
#   ./scripts/test.sh tests/test_rules.py
#   ./scripts/test.sh -k placeholder

set -euo pipefail
cd "$(dirname "$0")/.."

exec uv run pytest tests/ -v "$@"
