import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orcamento import MetaOrcamento
from Back_end.access_api.metas.models.meta_orgao import MetaOrgao
from Back_end.access_api.metas.models.orgao import Orgao
from Back_end.access_api.metas.models.meta_tag import MetaTag
from Back_end.access_api.metas.models.tag import Tag
from Back_end.access_api.metas.models.iniciativa import Iniciativa

from Back_end.access_api.metas.services.classification_service import (classify_meta_tags,)


def _format_money(value) -> str | None:
    """Formata um valor monetário no padrão brasileiro."""

    if value is None:
        return None

    formatted = (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {formatted}"


def get_meta_detail_by_codigo(codigo: str) -> dict | None:
    """
    Monta a Ficha da Meta a partir dos dados locais.

    Não consulta o SMAE.
    Retorna None quando o código não existe.
    """

    with rx.session() as session:
        # --------------------------------------------------
        # Meta
        # --------------------------------------------------

        meta = session.exec(
            select(Meta).where(
                Meta.codigo == codigo
            )
        ).first()

        if meta is None:
            return None

        if meta.id is None:
            raise RuntimeError(
                f"Meta {codigo} sem ID local."
            )

        # --------------------------------------------------
        # Tags e classificação
        # --------------------------------------------------

        tags = session.exec(
            select(Tag)
            .join(
                MetaTag,
                MetaTag.tag_id == Tag.id,
            )
            .where(
                MetaTag.meta_id == meta.id
            )
            .order_by(Tag.descricao)
        ).all()

        tag_descriptions = {
            tag.descricao
            for tag in tags
        }

        classification = classify_meta_tags(
            meta_id=meta.id,
            codigo=meta.codigo,
            descriptions=tag_descriptions,
        )

        ods = [
            tag.descricao
            for tag in tags
            if tag.descricao.startswith("ODS ")
        ]

        # Preservamos todas as tags para que os planos
        # e demais classificações possam ser exibidos
        # sem perder informações da fonte.
        todas_tags = [
            tag.descricao
            for tag in tags
        ]

        # --------------------------------------------------
        # Órgãos
        # --------------------------------------------------

        orgao_rows = session.exec(
            select(
                Orgao.sigla,
                Orgao.descricao,
                MetaOrgao.responsavel,
            )
            .join(
                MetaOrgao,
                MetaOrgao.orgao_id == Orgao.id,
            )
            .where(
                MetaOrgao.meta_id == meta.id
            )
            .order_by(Orgao.sigla)
        ).all()

        orgaos = [
            {
                "sigla": sigla or "",
                "descricao": descricao,
                "responsavel": responsavel,
            }
            for sigla, descricao, responsavel in orgao_rows
        ]

        # --------------------------------------------------
        # Orçamento
        # --------------------------------------------------

        orcamento = session.exec(
            select(MetaOrcamento).where(
                MetaOrcamento.meta_id == meta.id
            )
        ).first()

        orcamento_data = None

        if orcamento is not None:
            orcamento_data = {
                "previsao": _format_money(
                    orcamento.total_previsao
                ),
                "empenhado": _format_money(
                    orcamento.total_empenhado
                ),
                "liquidado": _format_money(
                    orcamento.total_liquidado
                ),
                "atualizado_em": (
                    orcamento.atualizado_em.isoformat()
                    if orcamento.atualizado_em is not None
                    else None
                ),
            }

        # --------------------------------------------------
        # Iniciativas
        # --------------------------------------------------

        iniciativas = session.exec(
            select(Iniciativa)
            .where(
                Iniciativa.meta_id == meta.id
            )
            .order_by(Iniciativa.codigo)
        ).all()

        iniciativas_data = [
            {
                "codigo": iniciativa.codigo,
                "titulo": iniciativa.titulo,
            }
            for iniciativa in iniciativas
        ]

        # --------------------------------------------------
        # Ficha
        # --------------------------------------------------

        return {
            "id": meta.id,
            "smae_id": meta.smae_id,
            "codigo": meta.codigo,
            "titulo": meta.titulo,
            "eixo": meta.tema_descricao or "",
            "contexto": meta.contexto or "",

            "andamento": classification.andamento,
            "situacao": classification.situacao,
            "prazo": classification.prazo,

            "orgaos": orgaos,
            "ods": ods,
            "tags": todas_tags,

            "orcamento": orcamento_data,
            "iniciativas": iniciativas_data,
        }