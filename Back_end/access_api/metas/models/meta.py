from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Retorna a data e hora atual em UTC."""
    return datetime.now(timezone.utc)


class Meta(SQLModel, table=True):
    """Representa uma Meta do Programa de Metas persistida no PDM V2."""

    __tablename__ = "metas"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # Identificação no SMAE
    smae_id: int = Field(
        sa_column=Column(
            Integer,
            unique=True,
            nullable=False,
            index=True,
        )
    )

    pdm_id: int = Field(index=True)

    codigo: str = Field(index=True)

    titulo: str = Field(
        sa_column=Column(
            Text,
            nullable=False,
        )
    )

    contexto: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    complemento: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    status: str | None = Field(
        default=None,
        index=True,
    )

    ativo: bool = Field(
        default=True,
        index=True,
    )

    # Macro tema
    macro_tema_smae_id: int | None = Field(
        default=None,
        index=True,
    )

    macro_tema_descricao: str | None = Field(
        default=None,
    )

    # Tema / eixo
    tema_smae_id: int | None = Field(
        default=None,
        index=True,
    )

    tema_descricao: str | None = Field(
        default=None,
    )

    # Subtema
    sub_tema_smae_id: int | None = Field(
        default=None,
        index=True,
    )

    sub_tema_descricao: str | None = Field(
        default=None,
    )

    # Cronograma
    cronograma_smae_id: int | None = Field(
        default=None,
    )

    atraso_grau: str | None = Field(
        default=None,
        index=True,
    )

    # Cópia sanitizada do retorno completo do SMAE.
    # Serve como segurança para informações que ainda não foram
    # normalizadas em tabelas próprias.
    raw_detail: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    synced_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )