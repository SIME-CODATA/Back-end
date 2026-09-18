from sqlalchemy import Column, ForeignKey, Integer, String
from sqlmodel import Field, SQLModel


class MetaEquipe(SQLModel, table=True):
    """
    Relaciona uma Meta às equipes referenciadas pelo SMAE.

    O nome/descrição da equipe ainda não está disponível
    nos dados atuais, então armazenamos o ID SMAE e o tipo.
    """

    __tablename__ = "meta_equipes"

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

    equipe_smae_id: int = Field(
        sa_column=Column(
            Integer,
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