"""Registros completos de monitoramento territorial da Meta.

ATENÇÃO: o parent abaixo reflete o HEAD descrito em 30/10/2026.
Confirme com `uv run alembic current` e `uv run alembic heads` antes de copiar
esta migration. Se a branch avançou, ajuste down_revision para o HEAD real.
"""
from alembic import op

revision = "f5d4a11c7e26"
down_revision = "77248e576909"
branch_labels = None
depends_on = None

SCHEMA = r'''
-- Execute no pgAdmin4 > Query Tool, no banco pdm_v2, ANTES de importar.
-- A migração é ADITIVA, não modifica cms_meta_contents nem dados já publicados.

CREATE TABLE IF NOT EXISTS public.cms_meta_geo_records (
  id SERIAL PRIMARY KEY,
  meta_code VARCHAR(30) NOT NULL REFERENCES public.cms_meta_contents(meta_code),
  external_code VARCHAR(100) NOT NULL DEFAULT '',
  source VARCHAR(32) NOT NULL DEFAULT 'planilha',
  source_key VARCHAR(200) NOT NULL,
  sheet_row INTEGER,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  source_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  draft_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  published_payload JSONB NULL,
  source_map JSONB NOT NULL DEFAULT '{}'::jsonb,
  pending_updates JSONB NOT NULL DEFAULT '{}'::jsonb,
  imported_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  published_at TIMESTAMPTZ,
  updated_by INTEGER,
  published_by INTEGER,
  CONSTRAINT uq_cms_meta_geo_source_key UNIQUE (source_key)
);
CREATE INDEX IF NOT EXISTS ix_cms_meta_geo_records_meta_code ON public.cms_meta_geo_records (meta_code);
CREATE INDEX IF NOT EXISTS ix_cms_meta_geo_records_external_code ON public.cms_meta_geo_records (external_code);
CREATE INDEX IF NOT EXISTS ix_cms_meta_geo_records_source ON public.cms_meta_geo_records (source);
CREATE INDEX IF NOT EXISTS ix_cms_meta_geo_records_is_active ON public.cms_meta_geo_records (is_active);
CREATE INDEX IF NOT EXISTS ix_cms_meta_geo_records_imported_at ON public.cms_meta_geo_records (imported_at);
CREATE INDEX IF NOT EXISTS ix_cms_meta_geo_code_active ON public.cms_meta_geo_records (meta_code, is_active);
CREATE TABLE IF NOT EXISTS public.cms_meta_geo_versions (
  id SERIAL PRIMARY KEY,
  geo_record_id INTEGER NOT NULL REFERENCES public.cms_meta_geo_records(id) ON DELETE CASCADE,
  version_number INTEGER NOT NULL,
  content JSONB NOT NULL DEFAULT '{}'::jsonb,
  source_map JSONB NOT NULL DEFAULT '{}'::jsonb,
  note VARCHAR(500) NOT NULL DEFAULT '',
  published_by INTEGER,
  published_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uq_cms_meta_geo_version UNIQUE (geo_record_id, version_number)
);
CREATE INDEX IF NOT EXISTS ix_cms_meta_geo_versions_geo_record_id ON public.cms_meta_geo_versions (geo_record_id);

'''


def upgrade():
    for statement in SCHEMA.split(";"):
        if statement.strip():
            op.execute(statement.strip())


def downgrade():
    # Downgrade consciente: remover tabelas apagará a geografia importada.
    raise RuntimeError("Downgrade bloqueado: faça backup e trate remoção de dados explicitamente.")
