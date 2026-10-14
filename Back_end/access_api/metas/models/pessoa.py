from sqlalchemy import Column, Integer, Text
from sqlmodel import Field, SQLModel


class Pessoa(SQLModel, table=True):
    """Representa uma pessoa referenciada pelo SMAE."""

    __tablename__ = "pessoas"

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

    nome_exibicao: str = Field(
        sa_column=Column(
            Text,
            nullable=False,
        )
    )