from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, SQLModel


class MetaTag(SQLModel, table=True):
    """Relaciona uma Meta às suas tags."""

    __tablename__ = "meta_tags"

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

    tag_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "tags.id",
                ondelete="CASCADE",
            ),
            primary_key=True,
        )
    )