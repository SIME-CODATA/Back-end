from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlmodel import Field, SQLModel


class MetaOrgao(SQLModel, table=True):
    """Relaciona uma Meta aos órgãos que participam dela."""

    __tablename__ = "meta_orgaos"

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

    orgao_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "orgaos.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        )
    )

    responsavel: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
            default=False,
        ),
    )