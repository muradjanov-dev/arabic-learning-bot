#!/usr/bin/env bash
# One-shot Railway deploy. Requires: railway login OR RAILWAY_TOKEN env var.
set -e

cd "$(dirname "$0")"

PROJECT_NAME="${PROJECT_NAME:-arabic-learning-bot}"
BOT_TOKEN="${BOT_TOKEN:-8724591968:AAHHrd5IzjWsh4Xt2elwFOxB53Ef4DfxBEE}"
ADMIN_IDS="${ADMIN_IDS:-917456291}"

echo "→ Checking Railway auth..."
railway whoami

echo "→ Initialising project '$PROJECT_NAME'..."
railway init -n "$PROJECT_NAME" || true

echo "→ Adding PostgreSQL..."
railway add --database postgres || true

echo "→ Setting env variables..."
railway variables --set "BOT_TOKEN=$BOT_TOKEN" \
                  --set "ADMIN_IDS=$ADMIN_IDS"

echo "→ Deploying..."
railway up --detach

echo "→ Reading public URL..."
railway domain || true

echo "✓ Done. Check your bot in Telegram."
