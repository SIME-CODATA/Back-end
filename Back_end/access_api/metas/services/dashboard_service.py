from collections import Counter, defaultdict
from decimal import Decimal

import reflex as rx
from sqlalchemy import func
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orcamento import ( MetaOrcamento,)
from Back_end.access_api.metas.services.classification_service import ( get_all_meta_classifications,)


def _percentage( value: int | Decimal, total: int | Decimal,) -> float:
    """Calcula percentual sem risco de divisão por zero."""

    if not total:
        return 0.0

    return round(
        float(value / total * 100),
        2,
    )


def get_dashboard_summary() -> dict:
    """
    Retorna os indicadores executivos utilizados pelo dashboard.

    Combina:
    - metas;
    - eixos;
    - classificação por tags;
    - orçamento;
    - última sincronização.
    """

    classifications = ( get_all_meta_classifications() )

    andamento = Counter(
        item.andamento
        for item in classifications
    )

    situacao = Counter(
        item.situacao
        for item in classifications
    )

    prazo = Counter(
        item.prazo
        for item in classifications
    )

    classification_by_meta_id = {
        item.meta_id: item
        for item in classifications
    }

    with rx.session() as session:
        total_metas = session.exec(
            select(
                func.count(Meta.id)
            )
        ).one()

        metas_ativas = session.exec(
            select(
                func.count(Meta.id)
            ).where(
                Meta.ativo == True  # noqa: E712
            )
        ).one()

        total_temas = session.exec(
            select(
                func.count(
                    func.distinct(
                        Meta.tema_smae_id
                    )
                )
            ).where(
                Meta.tema_smae_id.is_not(
                    None
                )
            )
        ).one()

        ultima_sincronizacao = (
            session.exec(
                select(
                    func.max(
                        Meta.synced_at
                    )
                )
            ).one()
        )

        metas_eixos = session.exec(
            select(
                Meta.id,
                Meta.tema_descricao,
            )
            .where(
                Meta.tema_descricao.is_not(
                    None
                )
            )
        ).all()

        orcamentos = session.exec(
            select(MetaOrcamento)
        ).all()

    # --------------------------------------------------
    # Eixos
    # --------------------------------------------------

    eixos_data = defaultdict(
        lambda: {
            "quantidade": 0,
            "atingidas": 0,
            "em_progresso": 0,
            "em_planejamento": 0,
        }
    )

    for meta_id, eixo in metas_eixos:
        if not eixo:
            continue

        data = eixos_data[eixo]

        data["quantidade"] += 1

        classification = (
            classification_by_meta_id.get(
                meta_id
            )
        )

        if classification is None:
            continue

        if (
            classification.andamento
            == "Atingida"
        ):
            data["atingidas"] += 1

        elif (
            classification.andamento
            == "Em progresso"
        ):
            data["em_progresso"] += 1

        elif (
            classification.andamento
            == "Em planejamento"
        ):
            data["em_planejamento"] += 1

    eixos_resumo = []

    for nome in sorted(eixos_data):
        data = eixos_data[nome]

        eixos_resumo.append(
            {
                "nome": nome,
                "quantidade": (
                    data["quantidade"]
                ),
                "atingidas": (
                    data["atingidas"]
                ),
                "em_progresso": (
                    data["em_progresso"]
                ),
                "em_planejamento": (
                    data["em_planejamento"]
                ),
                "percentual_atingidas": (
                    _percentage(
                        data["atingidas"],
                        data["quantidade"],
                    )
                ),
            }
        )

    # Mantemos este formato por compatibilidade
    # com a versão atual do DashboardState.
    metas_por_eixo = {
        item["nome"]: item["quantidade"]
        for item in eixos_resumo
    }

    # --------------------------------------------------
    # Orçamento
    # --------------------------------------------------

    zero = Decimal("0")

    total_previsao = sum(
        (
            item.total_previsao
            or zero
            for item in orcamentos
        ),
        zero,
    )

    total_empenhado = sum(
        (
            item.total_empenhado
            or zero
            for item in orcamentos
        ),
        zero,
    )

    total_liquidado = sum(
        (
            item.total_liquidado
            or zero
            for item in orcamentos
        ),
        zero,
    )

    metas_com_previsao = sum(
        1
        for item in orcamentos
        if (
            item.total_previsao
            is not None
            and item.total_previsao > 0
        )
    )

    metas_com_empenho = sum(
        1
        for item in orcamentos
        if (
            item.total_empenhado
            is not None
            and item.total_empenhado > 0
        )
    )

    metas_com_liquidacao = sum(
        1
        for item in orcamentos
        if (
            item.total_liquidado
            is not None
            and item.total_liquidado > 0
        )
    )

    metas_atingidas = andamento.get(
        "Atingida",
        0,
    )

    metas_em_progresso = andamento.get(
        "Em progresso",
        0,
    )

    metas_em_planejamento = andamento.get(
        "Em planejamento",
        0,
    )

    return {
        # Básico
        "total_metas": total_metas,
        "total_temas": total_temas,
        "metas_ativas": metas_ativas,
        "ultima_sincronizacao": (
            ultima_sincronizacao
        ),

        # Eixos
        "metas_por_eixo": metas_por_eixo,
        "eixos_resumo": eixos_resumo,

        # Andamento
        "metas_atingidas": metas_atingidas,
        "metas_em_progresso": (
            metas_em_progresso
        ),
        "metas_em_planejamento": (
            metas_em_planejamento
        ),

        "percentual_atingidas": (
            _percentage(
                metas_atingidas,
                total_metas,
            )
        ),

        "percentual_em_progresso": (
            _percentage(
                metas_em_progresso,
                total_metas,
            )
        ),

        "percentual_em_planejamento": (
            _percentage(
                metas_em_planejamento,
                total_metas,
            )
        ),

        # Classificações completas
        "andamento": dict(andamento),
        "situacao": dict(situacao),
        "prazo": dict(prazo),

        # Orçamento
        "orcamento": {
            "previsao": total_previsao,
            "empenhado": total_empenhado,
            "liquidado": total_liquidado,

            "percentual_empenhado": (
                _percentage(
                    total_empenhado,
                    total_previsao,
                )
            ),

            "percentual_liquidado": (
                _percentage(
                    total_liquidado,
                    total_previsao,
                )
            ),

            "metas_com_previsao": (
                metas_com_previsao
            ),
            "metas_com_empenho": (
                metas_com_empenho
            ),
            "metas_com_liquidacao": (
                metas_com_liquidacao
            ),
        },
    }