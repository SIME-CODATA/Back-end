#!/bin/sh
set -eu

echo "[PDM] Aplicando migrations..."
if [ -d "/app/alembic" ]; then
    uv run reflex db migrate
fi
# IMPORTANTE: migrations exigem revisão, backup e execução manual.
# NÃO executar `reflex db migrate` automaticamente em cada reinício.

echo '[PDM] Iniciando Reflex em produção, sob /backend/ ...'
exec uv run reflex run --env prod --loglevel info
