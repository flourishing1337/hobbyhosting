# ────────────────────────────────────────────────────────────────
# HobbyHosting ▸ Makefile
# Robust, framtidssäker och tydlig CLI för dev/prod/CI/CD
# ────────────────────────────────────────────────────────────────

# Konfig
COMPOSE_FILE        := config/docker-compose.yml
COMPOSE_PROFILE     ?= dev
DOCKER_COMPOSE      := docker compose -f $(COMPOSE_FILE)
DOCKER_BUILD_FLAGS  := --no-cache
ENV_FILE            := .env.$(COMPOSE_PROFILE)

# Generera fallback .env om saknas
ifeq (,$(wildcard $(ENV_FILE)))
$(shell echo "# fallback generated" > $(ENV_FILE))
endif

# Debug
ifdef VARS
$(info COMPOSE_FILE:      $(COMPOSE_FILE))
$(info COMPOSE_PROFILE:   $(COMPOSE_PROFILE))
$(info ENV_FILE:          $(ENV_FILE))
$(info DOCKER_COMPOSE:    $(DOCKER_COMPOSE))
endif

.DEFAULT_GOAL := help

.PHONY: help up down restart rebuild ps logs \
        restart-% logs-% rebuild-% \
        health-all health-auth health-mail health-ecom-backend health-ecom-frontend health-admin-frontend health-main-frontend \
        lint format test coverage-report \
        migrate seed-db backup-db \
        tag-release docker-push deploy \
        run-auth run-admin-fe run-ecom-fe \
        clean-all

## 📚 Hjälp: visa tillgängliga make-kommandon
help:
	@grep -E '^[a-zA-Z0-9_\-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

# ─── Compose: Bas ──────────────────────────────────────────────

up:                      ## Starta alla tjänster
	$(DOCKER_COMPOSE) --profile $(COMPOSE_PROFILE) up -d

down:                    ## Stoppa alla tjänster
	-$(DOCKER_COMPOSE) down

restart:                 ## Omstart (down + up)
	@$(MAKE) down
	@$(MAKE) up

rebuild:                 ## Bygg om allt (ingen cache) + starta
	$(DOCKER_COMPOSE) build $(DOCKER_BUILD_FLAGS)
	$(MAKE) up

ps:                      ## Visa container-status
	$(DOCKER_COMPOSE) ps

logs:                    ## Visa samlade loggar
	$(DOCKER_COMPOSE) logs -f --tail=100

# ─── Compose: Per tjänst ───────────────────────────────────────

restart-%:               ## Omstart av tjänst: make restart-auth_service
	$(DOCKER_COMPOSE) restart $*

logs-%:                  ## Loggar för tjänst: make logs-auth_service
	$(DOCKER_COMPOSE) logs -f $*

rebuild-%:               ## Rebuild enskild tjänst
	$(DOCKER_COMPOSE) build $(DOCKER_BUILD_FLAGS) $*
	$(DOCKER_COMPOSE) up -d $*

# ─── Healthchecks ──────────────────────────────────────────────

health-auth:             ## /auth/health internt via frontend-container
	docker exec -i hobbyhosting_frontend wget -qO- http://auth_service:8000/auth/health || echo "❌ auth_service"

health-mail:
	@curl -sf http://localhost:5000/health | jq . || echo "❌ mail_service"

health-ecom-backend:
	@curl -sf http://localhost:8001/health | jq . || echo "❌ ecom_backend"

health-ecom-frontend:
	@curl -sf http://localhost:3000/api/health | jq . || echo "❌ ecom_frontend"

health-admin-frontend:
	@curl -sf http://localhost:3100/api/health | jq . || echo "❌ admin_frontend"

health-main-frontend:
	@curl -sf http://localhost:8080/api/health | jq . || echo "❌ hobbyhosting_frontend"

health-all:              ## Kör alla health endpoints
	@echo "🔍 Kör health-checks..."
	@$(MAKE) health-auth
	@$(MAKE) health-mail
	@$(MAKE) health-ecom-backend
	@$(MAKE) health-ecom-frontend
	@$(MAKE) health-admin-frontend
	@$(MAKE) health-main-frontend
	@echo "✅  Klart."

# ─── Kodkvalitet ───────────────────────────────────────────────

lint:                    ## ESLint + Ruff
	npx eslint apps/**/src --max-warnings 0
	ruff check services

format:                  ## Prettier + Ruff + isort
	prettier -w "**/*.{js,jsx,ts,tsx,json,md,html,css}"
	ruff format services && ruff check --fix services
	isort services

test:                    ## Pytest + Jest
	./bin/pytest -q
	npx jest --coverage || true
	
coverage-report:         ## Visa HTML-rapport för coverage
	python -m webbrowser -t htmlcov/index.html || true

# ─── Databas ──────────────────────────────────────────────────

migrate:                 ## Alembic-migrering för alla
	alembic -c services/auth_service/alembic.ini upgrade head
	alembic -c services/mail_service/alembic.ini upgrade head
	alembic -c services/ecom/backend/alembic.ini upgrade head

seed-db:                 ## Fyll databas
	python services/database_service/init-scripts/seed.py

backup-db:               ## pg_dump backup
	mkdir -p backups
	docker exec -i database_service pg_dump -U $$POSTGRES_USER -Fc $$POSTGRES_DB \
		> backups/backup_$$(date +%F_%H-%M-%S).dump

# ─── CI/CD & Deploy ───────────────────────────────────────────

tag-release:             ## Skapa ny version + git-tag
	bash scripts/release.sh

docker-push:             ## Bygg & pusha Docker-images
	bash scripts/docker_push.sh

deploy:                  ## Full deploy: down + rebuild + status
	@$(MAKE) down
	@$(MAKE) rebuild
	@$(MAKE) ps

# ─── Lokalt dev ───────────────────────────────────────────────

run-auth:
	PYTHONPATH=$$(realpath services) \
	uvicorn auth_service.main:app --reload --host 0.0.0.0 --port 8000

run-admin-fe:
	cd services/admin_frontend && yarn dev --port 3100

run-ecom-fe:
	cd services/ecom/frontend && yarn dev --port 3000

# ─── Housekeeping ─────────────────────────────────────────────

clean-all:
	-$(DOCKER_COMPOSE) down -v --remove-orphans
	docker volume prune -f
	docker container prune -f
	docker image prune -f

promote-admin: ## Promota en användare till admin (kräver TOKEN och USERNAME)
	@echo "Promoting user $$USERNAME using token..."
	@if [ -z "$$TOKEN" ] || [ -z "$$USERNAME" ]; then \
		echo "❌ Du måste sätta TOKEN och USERNAME"; \
		echo "Exempel: make promote-admin TOKEN=... USERNAME=admin@example.com"; \
		exit 1; \
	fi; \
	curl -X POST https://auth.hobbyhosting.org/auth/promote \
	  -H "Content-Type: application/json" \
	  -H "Authorization: Bearer $$TOKEN" \
	  -d '{"username": "'$$USERNAME'"}'

list-users: ## Lista alla användare (kräver TOKEN)
	@echo "Hämtar användare med tillgångstoken..."
	@if [ -z "$$TOKEN" ]; then \
		echo "❌ Du måste sätta TOKEN. Exempel: make list-users TOKEN=..."; \
		exit 1; \
	fi; \
	curl -s -H "Authorization: Bearer $$TOKEN" https://auth.hobbyhosting.org/users | jq
