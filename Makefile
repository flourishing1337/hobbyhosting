# ────────────────────────────────────────────────────────────────────────────
# HobbyHosting ▸ Makefile
# Ett enda gränssnitt för att styra hela stacken – dev, prod, CI/CD, QA osv.
# ────────────────────────────────────────────────────────────────────────────

# ─── Konfiguration ───────────────────────────────────────────────────────────
COMPOSE_FILE       := config/docker-compose.yml
COMPOSE_PROFILE    ?= dev                      # dev/prod – exportera i CI, t.ex. PROD_PROFILE=prod
DOCKER_COMPOSE     := docker compose -f $(COMPOSE_FILE)
DOCKER_BUILD_FLAGS := --no-cache

# Visa variabler om man vill debugga
ifdef VARS
$(info COMPOSE_FILE:    $(COMPOSE_FILE))
$(info COMPOSE_PROFILE: $(COMPOSE_PROFILE))
$(info DC:              $(DOCKER_COMPOSE) --profile $(COMPOSE_PROFILE))
endif

# ─── Standardmål ─────────────────────────────────────────────────────────────
.DEFAULT_GOAL := help

.PHONY: help up down restart rebuild ps logs clean-all \
        restart-% logs-% rebuild-% \
        health-all health-auth health-mail health-ecom-backend health-ecom-frontend health-admin-frontend health-main-frontend \
        lint format test coverage-report \
        migrate seed-db backup-db \
        tag-release docker-push deploy \
        run-auth run-admin-fe run-ecom-fe \
        clean-all

# ─── Hjälp ────────────────────────────────────────────────────────────────────
help:                                   ## Visa denna hjälp
	@grep -E '^[a-zA-Z0-9_\-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

# ─── Docker Compose – Core ────────────────────────────────────────────────────
up:                                     ## Starta alla tjänster (profil=$(COMPOSE_PROFILE))
	$(DOCKER_COMPOSE) --profile $(COMPOSE_PROFILE) up -d

down:                                   ## Stoppa & ta ned alla containers
	$(DOCKER_COMPOSE) down

restart:                                ## Down + Up (snabb omstart)
	$(MAKE) down
	$(MAKE) up

rebuild:                                ## Bygg om allt utan cache + starta
	$(DOCKER_COMPOSE) build $(DOCKER_BUILD_FLAGS)
	$(MAKE) up

ps:                                     ## Lista containers
	$(DOCKER_COMPOSE) ps

logs:                                   ## Följ alla loggar (senaste 100 rader)
	$(DOCKER_COMPOSE) logs -f --tail 100

# ─── Docker Compose – per tjänst ─────────────────────────────────────────────
restart-%:                              ## Omstart av enstaka tjänst: make restart-auth_service
	$(DOCKER_COMPOSE) restart $*

logs-%:                                 ## Loggar för enstaka tjänst: make logs-auth_service
	$(DOCKER_COMPOSE) logs -f $*

rebuild-%:                              ## Bygg + start enstaka tjänst: make rebuild-auth_service
	$(DOCKER_COMPOSE) build $(DOCKER_BUILD_FLAGS) $*
	$(DOCKER_COMPOSE) up -d $*

# ─── Healthchecks ─────────────────────────────────────────────────────────────
health-auth:                           ## /health Auth service
	@curl -sf http://localhost:8000/health | jq . || echo "❌ auth_service"

health-mail:                           ## /health Mail service
	@curl -sf http://localhost:5000/health | jq . || echo "❌ mail_service"

health-ecom-backend:                   ## /health Ecom API
	@curl -sf http://localhost:8001/health | jq . || echo "❌ ecom_backend"

health-ecom-frontend:                  ## /api/health Ecom frontend
	@curl -sf http://localhost:3000/api/health | jq . || echo "❌ ecom_frontend"

health-admin-frontend:                 ## /api/health Admin frontend
	@curl -sf http://localhost:3100/api/health | jq . || echo "❌ admin_frontend"

health-main-frontend:                  ## /api/health Main frontend
	@curl -sf http://localhost:8080/api/health | jq . || echo "❌ hobbyhosting_frontend"

health-all:                            ## Kör alla health-checks
	@echo "🔍 Checking all /health endpoints..."
	@$(MAKE) health-auth
	@$(MAKE) health-mail
	@$(MAKE) health-ecom-backend
	@$(MAKE) health-ecom-frontend
	@$(MAKE) health-admin-frontend
	@$(MAKE) health-main-frontend

# ─── Kodkvalitet & tester ────────────────────────────────────────────────────
lint:                                  ## ESLint + Ruff
	@echo "🔍 Linting JS/TS…"
	@npx eslint apps/**/src services/**/src --max-warnings 0
	@echo "🔍 Linting Python…"
	@ruff check services
	@echo "✅ Lint OK"

format:                                ## Prettier + Ruff + isort
	@echo "🔧 Formatting JS/TS…"
	@prettier -w "**/*.{js,jsx,ts,tsx,json,md,html,css}"
	@echo "🔧 Formatting Python…"
	@ruff format services
	@ruff check --fix services
	@isort services

test:                                  ## PyTest + Jest
	@echo "🧪 Running Python tests…"
	@pytest -q
	@echo "🧪 Running JS tests…"
	@npx jest --coverage

coverage-report:                       ## Öppna Python HTML-coveragerapport
	@python -m webbrowser -t htmlcov/index.html || true

# ─── Databasverktyg ─────────────────────────────────────────────────────────
migrate:                              ## Alembic migrations (alla services)
	@alembic -c services/auth_service/alembic.ini upgrade head
	@alembic -c services/mail_service/alembic.ini upgrade head
	@alembic -c services/ecom/backend/alembic.ini upgrade head

seed-db:                              ## Initiera databas med seed-data
	@python services/database_service/init-scripts/seed.py

backup-db:                            ## pg_dump → backups/
	@mkdir -p backups
	@docker exec -i database_service pg_dump -U $$POSTGRES_USER -Fc $$POSTGRES_DB \
		> backups/backup_$$(date +%F_%H-%M-%S).dump && echo "🗄️ Backup klar"

# ─── CI/CD & Release ────────────────────────────────────────────────────────
tag-release:                          ## Skapa git-tag + changelog (skript)
	@bash scripts/release.sh

docker-push:                          ## Bygg & pusha docker-images
	@bash scripts/docker_push.sh

deploy:                               ## Down + rebuild + ps
	@$(MAKE) down
	@$(MAKE) rebuild
	@$(MAKE) ps

# ─── Lokal utveckling (kan tas bort i CI) ────────────────────────────────────
run-auth:                             ## Uvicorn Auth med hot-reload (port 8000)
	@PYTHONPATH=$$(realpath services) \
	  uvicorn auth_service.main:app --reload --host 0.0.0.0 --port 8000

run-admin-fe:                         ## Admin frontend med yarn dev (port 3100)
	@cd services/admin_frontend && yarn dev --port 3100

run-ecom-fe:                          ## Ecom frontend med yarn dev (port 3000)
	@cd services/ecom/frontend && yarn dev --port 3000

# ─── Housekeeping ───────────────────────────────────────────────────────────
clean-all:                            ## Rensa containers, volymer, images, cache
	@$(MAKE) down
	@docker volume prune -f
	@docker container prune -f
	@docker image prune -f
