"""Registro territorial/operacional associado a uma ficha CMS de Meta.

É separado de CmsMetaContent para preservar o versionamento editorial existente
(e evitar confundir linha de projeto com a Meta em si).
"""
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CmsMetaGeoRecord(SQLModel, table=True):
    __tablename__ = "cms_meta_geo_records"
    __table_args__ = (
        UniqueConstraint("source_key", name="uq_cms_meta_geo_source_key"),
        Index("ix_cms_meta_geo_code_active", "meta_code", "is_active"),
    )

    id: int | None = Field(default=None, primary_key=True)
    meta_code: str = Field(max_length=30, foreign_key="cms_meta_contents.meta_code", index=True)
    external_code: str = Field(default="", max_length=100, index=True)
    source: str = Field(default="planilha", max_length=32, index=True)
    source_key: str = Field(max_length=200)
    sheet_row: int | None = Field(default=None)
    is_active: bool = Field(default=True, index=True)

    # Captura integral e intocada da última fonte recebida.
    source_payload: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False)
    )
    # Conteúdo editável internamente, nunca publicado automaticamente.
    draft_payload: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False)
    )
    # None = nunca publicado; dicionário = publicação explícita.
    published_payload: dict[str, Any] | None = Field(
        default=None, sa_column=Column(JSONB, nullable=True)
    )
    # Por coluna original: 'planilha' | 'smae' | 'json' | 'manual'.
    source_map: dict[str, str] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False)
    )
    # Registro de atualizações que conflitam com valores alterados manualmente.
    pending_updates: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False)
    )
    imported_at: datetime = Field(default_factory=_utc_now, index=True)
    updated_at: datetime = Field(default_factory=_utc_now)
    published_at: datetime | None = Field(default=None)
    updated_by: int | None = Field(default=None)
    published_by: int | None = Field(default=None)
