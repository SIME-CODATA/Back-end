from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlmodel import Field, SQLModel


class MetaOrcamento(SQLModel, table=True):
    """Representa os dados orçamentários de uma Meta do SMAE."""

    __tablename__ = "meta_orcamentos"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # Uma meta possui no máximo um registro consolidado de orçamento.
    meta_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey(
                "metas.id",
                ondelete="CASCADE",
            ),
            unique=True,
            nullable=False,
            index=True,
        )
    )

    # Totais gerais
    total_previsao: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    total_empenhado: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    total_liquidado: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    # Projeto
    total_previsao_projeto: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    total_empenhado_projeto: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    total_liquidado_projeto: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    # Atividade
    total_previsao_atividade: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    total_empenhado_atividade: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    total_liquidado_atividade: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    # Operação especial
    total_previsao_operacao_especial: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    total_empenhado_operacao_especial: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    total_liquidado_operacao_especial: Decimal | None = Field(
        default=None,
        sa_column=Column(
            Numeric(18, 2),
            nullable=True,
        ),
    )

    # Data informada pelo próprio SMAE para atualização do orçamento
    atualizado_em: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )