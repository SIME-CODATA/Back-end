from typing import Any

from Back_end.site_cms.modules.metas.schema import (
    empty_meta_payload,
)


def normalize_smae_meta(
    raw_meta: dict[str, Any],
    *,
    initiatives: list[dict[str, Any]] | None = None,
    indicator: str | None = None,
    evolution: str | None = None,
    monitoring: str | None = None,
    measured_results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Normaliza uma Meta do SMAE para o contrato editorial do CMS.

    Os parâmetros opcionais permitem enriquecer o snapshot com dados
    vindos de outros endpoints/serviços do próprio SMAE sem acoplar
    este módulo ao client atual.
    """

    payload = empty_meta_payload()

    payload["number"] = str(
        raw_meta.get("codigo") or ""
    )

    payload["title"] = str(
        raw_meta.get("titulo") or ""
    )

    # O contexto do SMAE corresponde à projeção utilizada pelo site atual.
    payload["projection"] = str(
        raw_meta.get("contexto") or ""
    )

    participants = (
        raw_meta.get(
            "orgaos_participantes"
        )
        or []
    )

    payload["responsible_agencies"] = [
        str(
            (
                item.get("orgao")
                or {}
            ).get("sigla")
            or (
                item.get("orgao")
                or {}
            ).get("descricao")
            or ""
        )
        for item in participants
        if (
            item.get("responsavel")
            and (
                item.get("orgao")
                or {}
            )
        )
    ]

    theme = raw_meta.get("tema") or {}

    payload["axis_name"] = str(
        theme.get("descricao") or ""
    )

    payload["strategic_actions"] = [
        {
            "number": str(
                item.get("codigo") or ""
            ),
            "description": str(
                item.get("titulo")
                or item.get("descricao")
                or ""
            ),
            "completed": bool(
                item.get("concluida")
                or False
            ),
            "evolution_label": (
                item.get("evolucao_negrito")
            ),
            "evolution_description": (
                item.get(
                    "descricao_evolucao"
                )
            ),
        }
        for item in initiatives or []
    ]

    if indicator is not None:
        payload["indicator"] = indicator

    if evolution is not None:
        payload["evolution"] = evolution

    if monitoring is not None:
        payload["monitoring"] = monitoring

    if measured_results is not None:
        payload["measured_results"] = (
            measured_results
        )

    # Cores/frases do eixo e regionalização podem continuar sendo
    # complementos editoriais caso o SMAE ainda não forneça esses campos.

    return payload
