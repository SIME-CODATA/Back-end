import reflex as rx
from sqlalchemy import func
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta


def get_dashboard_summary() -> dict:
    """Retorna os indicadores básicos utilizados pelo dashboard."""

    with rx.session() as session:
        total_metas = session.exec(
            select(func.count(Meta.id))
        ).one()

        metas_ativas = session.exec(
            select(func.count(Meta.id)).where(
                Meta.ativo == True  # noqa: E712
            )
        ).one()

        total_temas = session.exec(
            select(
                func.count(
                    func.distinct(Meta.tema_smae_id)
                )
            ).where(
                Meta.tema_smae_id.is_not(None)
            )
        ).one()

        ultima_sincronizacao = session.exec(
            select(func.max(Meta.synced_at))
        ).one()

        metas_por_eixo_result = session.exec(
            select(
                Meta.tema_descricao,
                func.count(Meta.id),
            )
            .where(
                Meta.tema_descricao.is_not(None)
            )
            .group_by(
                Meta.tema_descricao
            )
            .order_by(
                Meta.tema_descricao
            )
        ).all()

        metas_por_eixo = {
            eixo: quantidade
            for eixo, quantidade in metas_por_eixo_result
            if eixo
        }

    return {
        "total_metas": total_metas,
        "total_temas": total_temas,
        "metas_ativas": metas_ativas,
        "ultima_sincronizacao": ultima_sincronizacao,
        "metas_por_eixo": metas_por_eixo,
    }