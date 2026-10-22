import re
from html import unescape
from typing import Any

from Back_end.site_cms.modules.metas.schema import (
    empty_meta_payload,
)


_TAG_RE = re.compile(r"<[^>]+>")


def _plain_text(value: Any) -> str:
    text = unescape(
        str(value or "")
    )
    return _TAG_RE.sub(
        "",
        text,
    ).strip()


def _media_reference(
    value: Any,
) -> dict[str, Any] | None:
    if value in (
        None,
        "",
    ):
        return None

    return {
        "media_id": None,
        "legacy_source": value,
    }


def _regionalization_block(
    *,
    key: str,
    title: str,
    data: dict[str, Any],
) -> dict[str, Any] | None:
    image = data.get("map_image")
    text = data.get("map_legenda")
    footer = data.get("map_rodape")

    has_content = any(
        value not in (
            None,
            "",
        )
        for value in (
            image,
            text,
            footer,
        )
    )

    if not has_content:
        return None

    return {
        "key": key,
        "title": title,
        "enabled": True,
        "image": _media_reference(
            image
        ),
        "text": str(
            text or ""
        ),
        "footer": str(
            footer or ""
        ),
        "buttons": [],
    }


def normalize_legacy_meta(
    raw_meta: dict[str, Any],
) -> dict[str, Any]:
    """
    Converte MetaResponseSchema da API antiga para o formato editorial
    interno do novo CMS.
    """

    payload = empty_meta_payload()

    card = raw_meta.get("card") or {}
    listing = raw_meta.get("listing") or {}

    payload["number"] = str(
        card.get("numero")
        or listing.get("numero")
        or ""
    )

    payload["title"] = _plain_text(
        listing.get("titulo")
    )

    projection = card.get("projecao") or {}
    payload["projection"] = str(
        projection.get("valor") or ""
    )

    actions = card.get(
        "acoes_estrategicas"
    ) or {}

    payload["strategic_actions"] = [
        {
            "number": str(
                item.get("numero") or ""
            ),
            "description": str(
                item.get("descricao") or ""
            ),
            "completed": bool(
                item.get("concluida")
            ),
            "evolution_label": (
                item.get("evolucao_negrito")
            ),
            "evolution_description": (
                item.get("descricao_evolucao")
            ),
        }
        for item in actions.get("valor") or []
    ]

    indicator = card.get(
        "indicador"
    ) or {}

    payload["indicator"] = str(
        indicator.get("valor") or ""
    )

    agencies = card.get(
        "orgaos_responsaveis"
    ) or {}

    payload["responsible_agencies"] = [
        str(value or "")
        for value in agencies.get("valor") or []
        if str(value or "").strip()
    ]

    payload["axis_name"] = str(
        card.get("eixo_nome") or ""
    )
    payload["axis_primary_color"] = str(
        card.get("eixo_cor_principal")
        or listing.get("eixo_cor_principal")
        or ""
    )
    payload["axis_secondary_color"] = str(
        card.get("eixo_cor_secundaria")
        or ""
    )
    payload["axis_phrases"] = [
        str(value or "")
        for value in (
            card.get("eixo_frase")
            or []
        )
        if str(value or "").strip()
    ]

    payload["evolution"] = str(
        card.get("evolucao") or ""
    )

    payload["monitoring"] = str(
        card.get("monitoramento")
        or ""
    )

    results = card.get(
        "resultados_apurados"
    ) or {}

    payload["measured_results"] = [
        {
            "value": str(
                item.get(
                    "resultados_apurados_value"
                )
                or ""
            ),
            "month": str(
                item.get("mes")
                or ""
            ),
            "year": item.get("ano"),
            "date": str(
                item.get("data")
                or ""
            ),
        }
        for item in results.get("valor") or []
    ]

    metamap = card.get(
        "regionalizacao_metamap"
    ) or {}
    planned = card.get(
        "regionalizacao_planejado"
    ) or {}
    executed = card.get(
        "regionalizacao_executado"
    ) or {}

    status = str(
        metamap.get(
            "status_regionalizacao"
        )
        or planned.get(
            "status_regionalizacao"
        )
        or executed.get(
            "status_regionalizacao"
        )
        or ""
    )

    if status == "não regionalizável":
        payload["regionalization"] = {
            "mode": "not_regionalizable",
            "note": metamap.get(
                "nota_regionalizacao"
            ),
            "blocks": [],
        }

    else:
        blocks = []

        planned_block = (
            _regionalization_block(
                key="planned",
                title="Planejado",
                data=planned,
            )
        )

        executed_block = (
            _regionalization_block(
                key="executed",
                title="Executado",
                data=executed,
            )
        )

        if planned_block:
            blocks.append(
                planned_block
            )

        if executed_block:
            blocks.append(
                executed_block
            )

        payload["regionalization"] = {
            "mode": "custom",
            "note": metamap.get(
                "nota_regionalizacao"
            ),
            "blocks": blocks,
        }

    return payload
