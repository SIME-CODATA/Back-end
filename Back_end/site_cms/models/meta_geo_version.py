"""Versões publicadas de cada linha do monitoramento territorial."""
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class CmsMetaGeoVersion(SQLModel, table=True):
    __tablename__ = "cms_meta_geo_versions"
    __table_args__ = (UniqueConstraint("geo_record_id", "version_number", name="uq_cms_meta_geo_version"),)
    id: int | None = Field(default=None, primary_key=True)
    geo_record_id: int = Field(foreign_key="cms_meta_geo_records.id", index=True)
    version_number: int = Field(default=1)
    content: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    source_map: dict[str, str] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    note: str = Field(default="", max_length=500)
    published_by: int | None = Field(default=None)
    published_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
