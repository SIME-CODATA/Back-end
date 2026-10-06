from typing import TypedDict
import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta


# ============================================================
# CONFIGURAÇÃO
# ============================================================

class MetaListItem(TypedDict):
    """Estrutura de uma meta utilizada na listagem."""

    codigo: str
    titulo: str
    eixo: str

    orgaos: list[str]
    temas: list[str]
    regioes: list[str]

    url: str

# No SMAE, as tags 214 a 229 representam os temas
# utilizados para classificar as metas.
THEME_TAG_IDS = set(range(214, 230))


# ============================================================
# HELPERS
# ============================================================

def _get_raw_detail(meta: Meta) -> dict:
    """Retorna o raw_detail da meta de forma segura."""

    raw_detail = meta.raw_detail

    if not isinstance(raw_detail, dict):
        return {}

    return raw_detail


def _extract_orgaos(raw_detail: dict) -> list[str]:
    """Extrai as siglas dos órgãos participantes."""

    orgaos: set[str] = set()

    participantes = (
        raw_detail.get("orgaos_participantes")
        or []
    )

    for participante in participantes:
        if not isinstance(participante, dict):
            continue

        orgao = participante.get("orgao") or {}

        if not isinstance(orgao, dict):
            continue

        nome = (
            orgao.get("sigla")
            or orgao.get("descricao")
        )

        if nome:
            orgaos.add(
                str(nome).strip()
            )

    return sorted(
        orgaos,
        key=str.casefold,
    )


def _extract_temas(raw_detail: dict) -> list[str]:
    """
    Extrai somente as tags temáticas do SMAE.

    As tags temáticas atuais utilizam IDs de 214 a 229.
    """

    temas: set[str] = set()

    tags = (
        raw_detail.get("tags")
        or []
    )

    for tag in tags:
        if not isinstance(tag, dict):
            continue

        tag_id = tag.get("id")

        try:
            tag_id = int(tag_id)
        except (TypeError, ValueError):
            continue

        if tag_id not in THEME_TAG_IDS:
            continue

        descricao = tag.get("descricao")

        if descricao:
            temas.add(
                str(descricao).strip()
            )

    return sorted(
        temas,
        key=str.casefold,
    )


def _extract_regioes(raw_detail: dict) -> list[str]:
    """
    Extrai regiões presentes nas geolocalizações da meta.

    O SMAE pode retornar regionalização em até quatro níveis.
    """

    regioes_encontradas: set[str] = set()

    geolocalizacoes = (
        raw_detail.get("geolocalizacao")
        or []
    )

    for geolocalizacao in geolocalizacoes:
        if not isinstance(
            geolocalizacao,
            dict,
        ):
            continue

        regioes = (
            geolocalizacao.get("regioes")
            or {}
        )

        if not isinstance(regioes, dict):
            continue

        for nivel in (
            "nivel_1",
            "nivel_2",
            "nivel_3",
            "nivel_4",
        ):
            itens = (
                regioes.get(nivel)
                or []
            )

            for item in itens:
                if not isinstance(
                    item,
                    dict,
                ):
                    continue

                descricao = item.get(
                    "descricao"
                )

                if descricao:
                    regioes_encontradas.add(
                        str(descricao).strip()
                    )

    return sorted(
        regioes_encontradas,
        key=str.casefold,
    )


# ============================================================
# LISTAGEM
# ============================================================

def list_metas() -> list[MetaListItem]:
    """
    Retorna as metas cadastradas com os dados
    necessários para listagem e filtros.
    """

    with rx.session() as session:
        metas = session.exec(select(Meta).order_by(    Meta.codigo)).all()

        resultado: list[MetaListItem] = []

        for meta in metas:
            raw_detail = _get_raw_detail(meta)

            resultado.append(
                {
                    "codigo": meta.codigo,
                    "titulo": meta.titulo,
                    # Hoje o tema_descricao do SMAE
                    # representa o eixo do PDM.
                    "eixo": (meta.tema_descricao or "Eixo não informado"),
                    # Dados utilizados pelos filtros.
                    "orgaos": _extract_orgaos(raw_detail),

                    "temas": _extract_temas(raw_detail),

                    "regioes": _extract_regioes(raw_detail),

                    "url": (
                        f"/admin/metas/"
                        f"{meta.codigo}"
                    ),
                }
            )

        return resultado