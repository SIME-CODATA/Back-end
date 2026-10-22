from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CmsSection(SQLModel, table=True):
    """Seção editável pertencente a uma página do CMS."""

    __tablename__ = "cms_sections"
    __table_args__ = (
        UniqueConstraint(
            "page_id",
            "key",
            name="uq_cms_sections_page_key",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    page_id: int = Field(
        foreign_key="cms_pages.id",
        index=True,
    )

    key: str = Field(
        max_length=100,
        index=True,
    )

    name: str = Field(
        max_length=160,
    )

    section_type: str = Field(
        max_length=100,
        index=True,
    )

    position: int = Field(
        default=0,
        index=True,
    )

    enabled: bool = Field(
        default=True,
        index=True,
    )

    status: str = Field(
        default="published",
        max_length=20,
        index=True,
    )

    draft_content: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(
            JSONB,
            nullable=False,
        ),
    )

    published_content: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(
            JSONB,
            nullable=False,
        ),
    )

    source_type: str = Field(
        default="manual",
        max_length=40,
        index=True,
    )

    source_endpoint: str | None = Field(
        default=None,
        max_length=500,
    )

    legacy_imported_at: datetime | None = Field(
        default=None,
    )

    created_by: int | None = Field(
        default=None,
        index=True,
    )

    updated_by: int | None = Field(
        default=None,
        index=True,
    )

    published_by: int | None = Field(
        default=None,
        index=True,
    )

    published_at: datetime | None = Field(
        default=None,
        index=True,
    )

    created_at: datetime = Field(
        default_factory=_utc_now,
        index=True,
    )

    updated_at: datetime = Field(
        default_factory=_utc_now,
        index=True,
    )
