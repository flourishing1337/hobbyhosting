#!/usr/bin/env bash
# Set up development and production env files if missing
# Usage: ./scripts/setup_env.sh [--force]

set -euo pipefail

force=0
if [[ "${1:-}" == "--force" ]]; then
  force=1
fi

for target in .env.dev .env.prod; do
  if [[ $force -eq 1 || ! -f "$target" ]]; then
    if [[ -f .env.example ]]; then
      cp .env.example "$target"
    else
      cat > "$target" <<'FEOF'
# POSTGRES_USER=
# POSTGRES_PASSWORD=
# AUTH_DB=
# MAIL_DB=
# ECOMMERCE_DB=
# RESEND_API_KEY=
# MAIL_FROM=
# JWT_SECRET=
# JWT_ALGO=HS256
FEOF
    fi
    echo "Created $target"
  fi
done
