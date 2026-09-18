from sqlalchemy import Column, Integer, Text
from sqlmodel import Field, SQLModel


class Tag(SQLModel, table=True):
    """Representa uma tag cadastrada no SMAE."""

    __tablename__ = "tags"

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

    descricao: str = Field(
        sa_column=Column(
            Text,
            nullable=False,
        )
    )