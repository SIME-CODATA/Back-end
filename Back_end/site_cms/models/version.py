from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CmsSectionVersion(SQLModel, table=True):
    """Snapshot publicado de uma seção do CMS."""

    __tablename__ = "cms_section_versions"
    __table_args__ = (
        UniqueConstraint(
            "section_id",
            "version_number",
            name="uq_cms_section_version",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    section_id: int = Field(
        foreign_key="cms_sections.id",
        index=True,
    )

    version_number: int = Field(
        index=True,
    )

    content: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(
            JSONB,
            nullable=False,
        ),
    )

    note: str = Field(
        default="",
        max_length=500,
    )

    published_by: int | None = Field(
        default=None,
        index=True,
    )

    published_at: datetime = Field(
        default_factory=_utc_now,
        index=True,
    )
