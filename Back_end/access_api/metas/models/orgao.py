from sqlalchemy import Column, Integer, Text
from sqlmodel import Field, SQLModel


class Orgao(SQLModel, table=True):
    """Representa um órgão cadastrado no SMAE."""

    __tablename__ = "orgaos"

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

    sigla: str | None = Field(
        default=None,
        index=True,
    )

    descricao: str = Field(
        sa_column=Column(
            Text,
            nullable=False,
        )
    )