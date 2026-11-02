from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MetaRelatedSnapshot(SQLModel, table=True):
    """Snapshot local dos objetos relacionados a uma Meta no SMAE.

    O SMAE continua sendo a fonte de atualização, mas o site público nunca
    depende de uma chamada ao SMAE para renderizar uma ficha ou um mapa.
    O payload bruto é preservado para que novos campos do SMAE possam ser
    aproveitados sem perda de informação.
    """

    __tablename__ = "meta_related_snapshots"

    id: int | None = Field(default=None, primary_key=True)

    meta_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("metas.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
            index=True,
        )
    )

    smae_meta_id: int = Field(index=True)

    payload: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONB, nullable=False),
    )

    geo_features: list[dict[str, Any]] = Field(
        default_factory=list,
        sa_column=Column(JSONB, nullable=False),
    )

    synced_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            index=True,
        ),
    )
