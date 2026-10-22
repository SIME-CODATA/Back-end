from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CmsMetaContent(SQLModel, table=True):
    """
    Camada editorial de uma Meta para o site público.

    meta_code é a identidade estável usada para relacionar o conteúdo
    editorial à Meta sincronizada do SMAE.

    smae_snapshot:
        última fotografia recebida do SMAE.

    draft_content:
        conteúdo efetivo em edição no CMS.

    published_content:
        última versão publicada para consumo do site.

    source_map:
        origem atual de cada campo do draft:
        - smae
        - cms
        - legacy
    """

    __tablename__ = "cms_meta_contents"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    meta_code: str = Field(
        max_length=30,
        unique=True,
        index=True,
    )

    smae_meta_id: int | None = Field(
        default=None,
        index=True,
    )

    status: str = Field(
        default="published",
        max_length=20,
        index=True,
    )

    smae_snapshot: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(
            JSONB,
            nullable=False,
        ),
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

    source_map: dict[str, str] = Field(
        default_factory=dict,
        sa_column=Column(
            JSONB,
            nullable=False,
        ),
    )

    legacy_snapshot: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(
            JSONB,
            nullable=False,
        ),
    )

    legacy_imported_at: datetime | None = Field(
        default=None,
        index=True,
    )

    smae_synced_at: datetime | None = Field(
        default=None,
        index=True,
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
