from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Iniciativa(SQLModel, table=True):
    """
    Representa uma iniciativa vinculada a uma Meta do PDM.

    Os dados são obtidos pelo endpoint:
    /meta/iniciativas-atividades
    """

    __tablename__ = "iniciativas"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    smae_id: int = Field(
        sa_column=Column(
            Integer,
            unique=True,
            nullable=False,
            index=True,
        )
    )

    meta_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "metas.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        )
    )

    codigo: str = Field(
        index=True,
    )

    titulo: str = Field(
        sa_column=Column(
            Text,
            nullable=False,
        )
    )

    raw_data: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )