from sqlalchemy import Column, ForeignKey, Integer, String
from sqlmodel import Field, SQLModel


class MetaPessoa(SQLModel, table=True):
    """
    Relaciona uma pessoa a uma Meta.

    O campo tipo indica o papel da pessoa dentro da Meta.
    """

    __tablename__ = "meta_pessoas"

    meta_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "metas.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        )
    )

    pessoa_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "pessoas.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        )
    )

    tipo: str = Field(
        sa_column=Column(
            String,
            primary_key=True,
            nullable=False,
        )
    )

    orgao_id: int | None = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey(
                "orgaos.id",
                ondelete="CASCADE",
            ),
            nullable=True,
        ),
    )