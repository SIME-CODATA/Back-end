#!/bin/sh
set -eu

echo "[PDM] Aplicando migrations..."
if [ -d "/app/alembic" ]; then
    uv run reflex db migrate
fi

echo "[PDM] Iniciando Reflex em modo produção..."
exec uv run reflex run --env prod --loglevel info
