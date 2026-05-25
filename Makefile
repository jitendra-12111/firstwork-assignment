# FirstWork — common dev commands.
#
# Usage:
#   make setup              # one-shot bootstrap (deps + db + migrations + seed)
#   make start              # run the API with reload
#   make test               # run pytest
#
# Migrations
#   make migrate            # apply all pending migrations (alembic upgrade head)
#   make migrate-new m="msg"  # create a new migration via autogenerate
#   make migrate-down       # roll back the last migration
#   make migrate-history    # show migration chain
#   make migrate-current    # show current DB revision
#
# Data
#   make seed               # reload docs/seed.sql
#
# Database
#   make db-shell           # open a mysql shell inside the container
#   make db-down            # stop the MySQL container (data persists)
#   make db-reset           # nuke the volume and re-run setup (DESTRUCTIVE)
#
# Housekeeping
#   make clean              # remove .venv and __pycache__

.PHONY: setup start test migrate migrate-new migrate-down migrate-history migrate-current \
        seed db-shell db-down db-reset clean

setup:
	./scripts/setup.sh

start:
	./scripts/start.sh

test:
	./scripts/test.sh

# ── Migrations ──────────────────────────────────────────────────────────

migrate:
	uv run alembic upgrade head

migrate-new:
	@if [ -z "$(m)" ]; then \
		echo "Usage: make migrate-new m=\"add column X to Y\""; \
		exit 1; \
	fi
	uv run alembic revision --autogenerate -m "$(m)"

migrate-down:
	uv run alembic downgrade -1

migrate-history:
	uv run alembic history

migrate-current:
	uv run alembic current

# ── Data ────────────────────────────────────────────────────────────────

seed:
	docker compose exec -T db mysql -u root -psecret firstwork < docs/seed.sql

# ── Database ────────────────────────────────────────────────────────────

db-shell:
	docker compose exec db mysql -u root -psecret firstwork

db-down:
	docker compose down

db-reset:
	docker compose down -v
	$(MAKE) setup

# ── Housekeeping ────────────────────────────────────────────────────────

clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
