from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CmsMetaSyncConflict(SQLModel, table=True):
    """
    Conflito entre uma personalização do CMS e uma mudança recebida do SMAE.

    Um conflito fica pending até o usuário escolher:
    - keep_cms
    - use_smae
    """

    __tablename__ = "cms_meta_sync_conflicts"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    meta_content_id: int = Field(
        foreign_key="cms_meta_contents.id",
        index=True,
    )

    field_key: str = Field(
        max_length=100,
        index=True,
    )

    reason: str = Field(
        default="changed_in_smae",
        max_length=60,
        index=True,
    )

    previous_smae_value: Any | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )

    incoming_smae_value: Any | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )

    cms_value: Any | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )

    status: str = Field(
        default="pending",
        max_length=20,
        index=True,
    )

    decision: str | None = Field(
        default=None,
        max_length=20,
        index=True,
    )

    detected_at: datetime = Field(
        default_factory=_utc_now,
        index=True,
    )

    resolved_at: datetime | None = Field(
        default=None,
        index=True,
    )

    resolved_by: int | None = Field(
        default=None,
        index=True,
    )
