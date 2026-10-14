from typing import TypedDict

import reflex as rx

from sqlmodel import select

from Back_end.access_api.metas.models.meta import (
    Meta,
)

from Back_end.access_api.smae.services.meta_service import (
    fetch_relacionados_by_meta_ids,
)


# ============================================================
# TIPAGEM
# ============================================================

class MetaListItem(TypedDict):
    """Estrutura de uma meta utilizada na listagem."""

    codigo: str

    titulo: str

    eixo: str

    orgaos: list[str]

    temas: list[str]

    status: str

    projecao: str

    regioes: list[str]

    url: str


# ============================================================
# CONFIGURAÇÃO
# ============================================================

# Tags temáticas do SMAE.
THEME_TAG_IDS = set(
    range(
        214,
        230,
    )
)


# ------------------------------------------------------------
# Status / andamento
# ------------------------------------------------------------

STATUS_NORMALIZATION = {
    "em planejamento": (
        "Em planejamento"
    ),

    "em progresso": (
        "Em progresso"
    ),

    "atingida": (
        "Atingida/Concluída"
    ),

    "atingida/concluída": (
        "Atingida/Concluída"
    ),

    "atingida/concluida": (
        "Atingida/Concluída"
    ),
}


# ------------------------------------------------------------
# Projeção de entrega
# ------------------------------------------------------------

PROJECAO_VALUES = {
    "1º sem/2025",
    "2º sem/2025",

    "1º sem/2026",
    "2º sem/2026",

    "1º sem/2027",
    "2º sem/2027",

    "1º sem/2028",
    "2º sem/2028",

    "Sem previsão",
}


# ------------------------------------------------------------
# Região
# ------------------------------------------------------------

REGIOES_POR_PARENTE_ID = {
    181: "Zona Leste",
    182: "Zona Norte",
    183: "Zona Sul",
    184: "Zona Oeste",
    185: "Centro",
}


# ============================================================
# HELPERS
# ============================================================

def _get_raw_detail(
    meta: Meta,
) -> dict:
    """Retorna raw_detail de forma segura."""

    raw_detail = (
        meta.raw_detail
    )

    if not isinstance(
        raw_detail,
        dict,
    ):
        return {}

    return raw_detail


# ============================================================
# TAGS
# ============================================================

def _get_tags(
    raw_detail: dict,
) -> list[dict]:
    """Retorna somente tags válidas."""

    tags = (
        raw_detail.get(
            "tags"
        )
        or []
    )

    if not isinstance(
        tags,
        list,
    ):
        return []

    return [
        tag

        for tag in tags

        if isinstance(
            tag,
            dict,
        )
    ]


# ============================================================
# ÓRGÃOS
# ============================================================

def _extract_orgaos(
    raw_detail: dict,
) -> list[str]:
    """Extrai siglas dos órgãos participantes."""

    orgaos: set[str] = set()

    participantes = (
        raw_detail.get(
            "orgaos_participantes"
        )
        or []
    )

    if not isinstance(
        participantes,
        list,
    ):
        return []

    for participante in participantes:

        if not isinstance(
            participante,
            dict,
        ):
            continue

        orgao = (
            participante.get(
                "orgao"
            )
            or {}
        )

        if not isinstance(
            orgao,
            dict,
        ):
            continue

        nome = (
            orgao.get(
                "sigla"
            )
            or orgao.get(
                "descricao"
            )
        )

        if nome:
            orgaos.add(
                str(nome).strip()
            )

    return sorted(
        orgaos,
        key=str.casefold,
    )


# ============================================================
# TEMAS
# ============================================================

def _extract_temas(
    raw_detail: dict,
) -> list[str]:
    """
    Extrai somente as tags temáticas do SMAE.

    As tags temáticas atuais utilizam IDs
    de 214 a 229.
    """

    temas: set[str] = set()

    tags = _get_tags(
        raw_detail
    )

    for tag in tags:

        tag_id = (
            tag.get(
                "id"
            )
        )

        try:
            tag_id = int(
                tag_id
            )

        except (
            TypeError,
            ValueError,
        ):
            continue

        if (
            tag_id
            not in THEME_TAG_IDS
        ):
            continue

        descricao = (
            tag.get(
                "descricao"
            )
        )

        if descricao:

            temas.add(
                str(
                    descricao
                ).strip()
            )

    return sorted(
        temas,
        key=str.casefold,
    )


# ============================================================
# STATUS
# ============================================================

def _extract_status(
    raw_detail: dict,
) -> str:
    """
    Extrai o status de andamento da meta.

    Exemplos:
    - Em planejamento
    - Em progresso
    - Atingida/Concluída
    """

    tags = _get_tags(
        raw_detail
    )

    for tag in tags:

        descricao = str(
            tag.get(
                "descricao"
            )
            or ""
        ).strip()

        if not descricao:
            continue

        normalized = (
            descricao.casefold()
        )

        status = (
            STATUS_NORMALIZATION
            .get(
                normalized
            )
        )

        if status:
            return status

    return "Não informado"


# ============================================================
# PROJEÇÃO
# ============================================================

def _extract_projecao(
    raw_detail: dict,
) -> str:
    """
    Extrai a projeção/previsão de entrega
    registrada nas tags da meta.
    """

    tags = _get_tags(
        raw_detail
    )

    for tag in tags:

        descricao = str(
            tag.get(
                "descricao"
            )
            or ""
        ).strip()

        if (
            descricao
            in PROJECAO_VALUES
        ):
            return descricao

    return "Sem previsão"


# ============================================================
# REGIONALIZAÇÃO
# ============================================================

def _extract_regioes_from_relacionados(
    relacionados: dict,
) -> list[str]:
    """
    Extrai regiões a partir das subprefeituras
    das obras relacionadas à meta.

    Não representa necessariamente uma região
    oficial cadastrada diretamente na meta.
    """

    regioes: set[str] = set()

    obras = (
        relacionados.get(
            "obras"
        )
        or []
    )

    if not isinstance(
        obras,
        list,
    ):
        return []

    for obra in obras:

        if not isinstance(
            obra,
            dict,
        ):
            continue

        subprefeituras = (
            obra.get(
                "subprefeituras"
            )
            or []
        )

        if not isinstance(
            subprefeituras,
            list,
        ):
            continue

        for subprefeitura in (
            subprefeituras
        ):

            if not isinstance(
                subprefeitura,
                dict,
            ):
                continue

            parente_id = (
                subprefeitura.get(
                    "parente_id"
                )
            )

            try:
                parente_id = int(
                    parente_id
                )

            except (
                TypeError,
                ValueError,
            ):
                continue

            regiao = (
                REGIOES_POR_PARENTE_ID
                .get(
                    parente_id
                )
            )

            if regiao:
                regioes.add(
                    regiao
                )

    return sorted(
        regioes,
        key=str.casefold,
    )


# ============================================================
# LISTAGEM
# ============================================================

def list_metas() -> list[
    MetaListItem
]:
    """
    Retorna metas cadastradas com os dados
    necessários para listagem e filtros.

    A regionalização continua sendo obtida
    das obras relacionadas no SMAE.

    Status e projeção são obtidos do
    raw_detail já armazenado localmente.
    """

    # --------------------------------------------------------
    # Metas locais
    # --------------------------------------------------------

    with rx.session() as session:

        metas = session.exec(
            select(
                Meta
            ).order_by(
                Meta.codigo
            )
        ).all()

    # --------------------------------------------------------
    # IDs SMAE
    # --------------------------------------------------------

    meta_ids = [
        meta.smae_id

        for meta in metas

        if (
            meta.smae_id
            is not None
        )
    ]

    # --------------------------------------------------------
    # Relacionados
    # --------------------------------------------------------

    relacionados_por_meta: dict[
        int,
        dict,
    ] = {}

    if meta_ids:

        try:
            relacionados_por_meta = (
                fetch_relacionados_by_meta_ids(
                    meta_ids
                )
            )

        except Exception as error:

            # A listagem continua funcionando
            # mesmo se o SMAE estiver indisponível.

            print(
                "Erro ao carregar regiões "
                f"das metas: {error}"
            )

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    resultado: list[
        MetaListItem
    ] = []

    for meta in metas:

        raw_detail = (
            _get_raw_detail(
                meta
            )
        )

        relacionados = {}

        if (
            meta.smae_id
            is not None
        ):

            relacionados = (
                relacionados_por_meta.get(
                    meta.smae_id,
                    {},
                )
            )

        resultado.append(
            {
                "codigo": (
                    meta.codigo
                ),

                "titulo": (
                    meta.titulo
                ),

                # Hoje tema_descricao representa
                # o eixo do Programa de Metas.

                "eixo": (
                    meta.tema_descricao
                    or "Eixo não informado"
                ),

                "orgaos": (
                    _extract_orgaos(
                        raw_detail
                    )
                ),

                "temas": (
                    _extract_temas(
                        raw_detail
                    )
                ),

                "status": (
                    _extract_status(
                        raw_detail
                    )
                ),

                "projecao": (
                    _extract_projecao(
                        raw_detail
                    )
                ),

                "regioes": (
                    _extract_regioes_from_relacionados(
                        relacionados
                    )
                ),

                "url": (
                    f"/admin/metas/"
                    f"{meta.codigo}"
                ),
            }
        )

    return resultado