# ────────────────────────────────────────────────────────────
# HobbyHosting ▸ Makefile
# One command-line to rule them all
# ────────────────────────────────────────────────────────────

COMPOSE_FILE          = ./config/docker-compose.yml
DOCKER_COMPOSE        = docker compose -f $(COMPOSE_FILE)
DOCKER_BUILD_FLAGS    = --no-cache
DOCKER_DEFAULT_PROFILE?=dev                                # ändra till "prod" i t.ex. CI

# --- Make prints vars bara om man kör: make VARS=1
ifdef VARS
$(info COMPOSE_FILE:      $(COMPOSE_FILE))
$(info DOCKER_COMPOSE:    $(DOCKER_COMPOSE))
endif

# ────────────────────────────────────────────────────────────
# HELP (typ  `make`  eller  `make help`)
# ────────────────────────────────────────────────────────────
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z0-9_\-]+:.*?## .*$$' \
		$(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-24s\033[0m %s\n", $$1, $$2}'

# ────────────────────────────────────────────────────────────
# DOCKER COMPOSE – CORE
# ────────────────────────────────────────────────────────────
up:             ## Starta alla tjänster i bakgrunden
	$(DOCKER_COMPOSE) --profile $(DOCKER_DEFAULT_PROFILE) up -d

down:           ## Stoppa & ta ned alla kontainrar
	$(DOCKER_COMPOSE) down

restart:        ## Snabb-omstart av alla kontainrar
	$(MAKE) down && $(MAKE) up

rebuild:        ## Bygg om allt (ingen cache) + starta
	$(DOCKER_COMPOSE) build $(DOCKER_BUILD_FLAGS)
	$(DOCKER_COMPOSE) up -d

ps:             ## Lista kontainrar
	$(DOCKER_COMPOSE) ps

logs:           ## Följ loggar
	$(DOCKER_COMPOSE) logs -f --tail=100

# ────────────────────────────────────────────────────────────
# DOCKER COMPOSE – PER-TJÄNST
# ────────────────────────────────────────────────────────────
restart-%:      ## make restart-SERVICE   »  omstart av tjänst
	$(DOCKER_COMPOSE) restart $*

logs-%:         ## make logs-SERVICE      »  loggar för tjänst
	$(DOCKER_COMPOSE) logs -f $*

rebuild-%:      ## make rebuild-SERVICE   »  bygg + start enstaka
	$(DOCKER_COMPOSE) build $(DOCKER_BUILD_FLAGS) $*
	$(DOCKER_COMPOSE) up -d $*

# ────────────────────────────────────────────────────────────
# HEALTHCHECK SHORTCUTS
# ────────────────────────────────────────────────────────────
health-auth:    ## Snabb hälsokoll Auth
	curl -sf http://localhost:8000/health | jq . || echo "❌ Auth FAILED"

health-mail:    ## Snabb hälsokoll Mail
	curl -sf http://localhost:5000/health | jq . || echo "❌ Mail FAILED"

health-ecom:    ## Snabb hälsokoll E-commerce backend
	curl -sf http://localhost:8001/health | jq . || echo "❌ Ecom FAILED"

# ────────────────────────────────────────────────────────────
# QUALITY (lokala verktyg – inga kontainrar behövs)
# ────────────────────────────────────────────────────────────
lint:           ## ESLint + Ruff + Prettier check
	@echo "🔍  Linting JS/TS…"; \
		npx eslint apps/**/src services/**/src --max-warnings 0
	@echo "🔍  Linting Python…"; \
		ruff check services
	@echo "✅  Lint OK"

format:         ## Formatera kod (Prettier + Ruff + isort)
	@prettier -w "**/*.{js,jsx,ts,tsx,json,md,html,css}"
	@ruff format services
	@ruff check --fix services
	@isort services

test:           ## Kör alla tester (PyTest + Jest)
	@pytest -q
	@npx jest --coverage

coverage-report: ## Öppna HTML-testrapport lokalt
	@python -m webbrowser -t htmlcov/index.html || true

# ────────────────────────────────────────────────────────────
# DATABASE UTILITIES
# ────────────────────────────────────────────────────────────
migrate:        ## Alembic migration (Auth, Mail, Ecom)
	@alembic -c services/auth_service/alembic.ini upgrade head
	@alembic -c services/mail_service/alembic.ini upgrade head
	@alembic -c services/ecom/backend/alembic.ini upgrade head

seed-db:        ## Fyll databasen med startdata
	@python services/database_service/init-scripts/seed.py

backup-db:      ## PGa_dump till ./backups/…
	@mkdir -p backups
	@docker exec database_service pg_dump -U $$POSTGRES_USER -Fc $$POSTGRES_DB \
		> backups/backup_$$(date +%F_%H-%M-%S).dump
	@echo "🗄️  Backup klar."

# ────────────────────────────────────────────────────────────
# DEPLOY & RELEASE (exempel – justera till er CI/CD)
# ────────────────────────────────────────────────────────────
tag-release:    ## Skapa git-tag + changelog (semver)
	@bash scripts/release.sh

docker-push:    ## Bygg & pusha images till registry
	@bash scripts/docker_push.sh

deploy:         ## Gör clean, rebuild & visa status
	$(MAKE) down
	$(MAKE) rebuild
	$(MAKE) ps

# ────────────────────────────────────────────────────────────
# LOCAL DEV SHORTCUTS (om man absolut måste köra lokalt)
# ────────────────────────────────────────────────────────────
run-auth:       ## Uvicorn Auth med hot-reload (host:8000)
	PYTHONPATH=$$(realpath services) uvicorn auth_service.main:app \
		--reload --host 0.0.0.0 --port 8000

run-admin-fe:   ## Yarn dev för Admin-frontend (host:3100)
	cd services/admin_frontend && yarn dev --port 3100

# ────────────────────────────────────────────────────────────
# HOUSEKEEPING
# ────────────────────────────────────────────────────────────
clean-all:      ## Docker down + rensa volymer & orphan-cont.
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker volume prune -f
	docker image prune -f
	docker container prune -f

.PHONY: help up down restart rebuild ps logs \
	restart-% logs-% rebuild-% \
	health-auth health-mail health-ecom \
	lint format test coverage-report \
	migrate seed-db backup-db \
	tag-release docker-push deploy \
	run-auth run-admin-fe \
	clean-all
	@echo "🔍 Checking Auth...";      curl -sf http://localhost:8000/health           && echo "✅"
	@echo "🔍 Checking Mail...";      curl -sf http://localhost:5000/health           && echo "✅"
	@echo "🔍 Checking Ecom API...";  curl -sf http://localhost:8001/health           && echo "✅"
	@echo "🔍 Checking Frontends…"
	@curl -sf http://localhost:3100/api/health || true  # admin
	@curl -sf http://localhost:3000/api/health || true  # ecom
	@curl -sf http://localhost:8080/api/health || true  # main
	@echo "🏁  All done"

## 🔍 Pinga alla /health endpoints
	@echo "Auth:"     && curl -sf http://localhost:8000/health  && echo OK
	@echo "Mail:"     && curl -sf http://localhost:5000/health  && echo OK
	@echo "Ecom API:" && curl -sf http://localhost:8001/health  && echo OK
	@echo "Admin FE:" && curl -sf http://localhost:3100/api/health && echo OK
	@echo "Ecom FE:"  && curl -sf http://localhost:3000/api/health && echo OK
	@echo "Main FE:"  && curl -sf http://localhost:8080/api/health && echo OK
	@echo "🏁 Done"

## 🔍 Pinga alla /health endpoints
	@echo "Auth:"     && curl -sf http://localhost:8000/health  && echo OK
	@echo "Mail:"     && curl -sf http://localhost:5000/health  && echo OK
	@echo "Ecom API:" && curl -sf http://localhost:8001/health  && echo OK
	@echo "Admin FE:" && curl -sf http://localhost:3100/api/health && echo OK
	@echo "Ecom FE:"  && curl -sf http://localhost:3000/api/health && echo OK
	@echo "Main FE:"  && curl -sf http://localhost:8080/api/health && echo OK
	@echo "🏁 Done"

## 🔍 Pinga alla /health endpoints
	@echo "Auth:"     && curl -sf http://localhost:8000/health  && echo OK
	@echo "Mail:"     && curl -sf http://localhost:5000/health  && echo OK
	@echo "Ecom API:" && curl -sf http://localhost:8001/health  && echo OK
	@echo "Admin FE:" && curl -sf http://localhost:3100/api/health && echo OK
	@echo "Ecom FE:"  && curl -sf http://localhost:3000/api/health && echo OK
	@echo "Main FE:"  && curl -sf http://localhost:8080/api/health && echo OK
	@echo "🏁 Done"

.PHONY: health-check
## 🔍 Pinga alla /health endpoints
health-check:
	@echo "Auth:"     && curl -sf http://localhost:8000/health  && echo OK
	@echo "Mail:"     && curl -sf http://localhost:5000/health  && echo OK
	@echo "Ecom API:" && curl -sf http://localhost:8001/health  && echo OK
	@echo "Admin FE:" && curl -sf http://localhost:3100/api/health && echo OK
	@echo "Ecom FE:"  && curl -sf http://localhost:3000/api/health && echo OK
	@echo "Main FE:"  && curl -sf http://localhost:8080/api/health && echo OK
	@echo "🏁 Done"
