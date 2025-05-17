#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Kör alla patchar..."

# ─── 1) Health‐endpoint på Python‐tjänster ─────────────────
for svc in auth_service mail_service; do
  if [ "$svc" = "auth_service" ]; then
    FILE="services/auth_service/main.py"
  else
    FILE="services/mail_service/app/main.py"
  fi

  if ! grep -q "def health" "$FILE" 2>/dev/null; then
    cat >> "$FILE" << 'PYTHON'

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
PYTHON
    echo "  ✓ Patcherade $FILE"
  fi
done

# ─── 2) Health‐endpoint i Ecom backend ─────────────────────
EFILE="services/ecom/backend/app/main.py"
if ! grep -q "def health" "$EFILE" 2>/dev/null; then
  cat >> "$EFILE" << 'PYTHON'

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
PYTHON
  echo "  ✓ Patcherade $EFILE"
fi

# ─── 3) Health‐endpoint i Next‐frontends ──────────────────
for FE in services/admin_frontend services/ecom/frontend apps/hobbyhosting-frontend; do
  # next/pages/api
  API_DIR="$FE/src/pages/api"
  if [ -d "$API_DIR" ]; then
    mkdir -p "$API_DIR"
    cat > "$API_DIR/health.ts" << 'TS'
import type { NextApiRequest, NextApiResponse } from "next";
export default function handler(_: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ status: "ok" });
}
TS
    echo "  ✓ Skapade $API_DIR/health.ts"
    continue
  fi

  # next/app/api
  APP_API_DIR="$FE/src/app/api/health"
  if [ -d "$(dirname "$APP_API_DIR")" ]; then
    mkdir -p "$APP_API_DIR"
    cat > "$APP_API_DIR/route.ts" << 'TS'
import { NextResponse } from "next/server";
export function GET() {
  return NextResponse.json({ status: "ok" });
}
TS
    echo "  ✓ Skapade $APP_API_DIR/route.ts"
  fi
done

# ─── 4) Generera .env.dev & .env.prod ────────────────────
for ENVF in .env.dev .env.prod; do
  if [ ! -f "$ENVF" ]; then
    if [ -f .env ]; then
      cp .env "$ENVF"
    elif [ -f .env.example ]; then
      cp .env.example "$ENVF"
    else
      cat > "$ENVF" << 'EOF'
# ⚠️ Fyll i era miljö-variabler här
# POSTGRES_USER=
# POSTGRES_PASSWORD=
# AUTH_DB=
# MAIL_DB=
# ECOM_DB=
EOF
    fi
    echo "  ✓ Skapade $ENVF"
  fi
done

# ─── 5) Makefile: endast en .PHONY och nytt health‐mål ────
MF=Makefile

# Ta bort gamla health‐sektioner
grep -v '^health-check:' "$MF" | grep -v '^[[:space:]]*# health-check' > tmp && mv tmp "$MF"

# Slå ihop alla .PHONY‐rader
awk '
  /^\.PHONY:/ { if(!p++){ print; } next }
  { print }
' "$MF" > tmp && mv tmp "$MF"

# Lägg till health‐check längst ned
cat >> "$MF" << 'MAKE'

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
MAKE

echo "  ✓ Makefile uppdaterad"

# ─── 6) Kör pre-commit, commit & push ─────────────────────
git add scripts/apply_all.sh Makefile .env.dev .env.prod
if command -v pre-commit &>/dev/null; then
  pre-commit run --all-files
  git add -A
  git commit -m "chore: add /health endpoints + health-check target + env.dev/prod"
  git push
  echo "✅ Allt klart och pushed!"
else
  echo "⚠ pre-commit not found – run manually:"
  echo "    git add -A && pre-commit run --all-files && git add -A && git commit -m '...' && git push"
fi
