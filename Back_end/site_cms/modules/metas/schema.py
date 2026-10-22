from typing import Any


META_FIELD_KEYS = [
    "number",
    "title",
    "projection",
    "strategic_actions",
    "indicator",
    "responsible_agencies",
    "axis_name",
    "axis_primary_color",
    "axis_secondary_color",
    "axis_phrases",
    "evolution",
    "monitoring",
    "measured_results",
    "regionalization",
]


FIELD_LABELS = {
    "number": "Número da Meta",
    "title": "Título",
    "projection": "Projeção",
    "strategic_actions": "Ações estratégicas",
    "indicator": "Indicador",
    "responsible_agencies": "Órgãos responsáveis",
    "axis_name": "Eixo",
    "axis_primary_color": "Cor principal do eixo",
    "axis_secondary_color": "Cor secundária do eixo",
    "axis_phrases": "Textos do eixo",
    "evolution": "Evolução",
    "monitoring": "Monitoramento",
    "measured_results": "Resultados apurados",
    "regionalization": "Regionalização",
}


def empty_meta_payload() -> dict[str, Any]:
    return {
        "number": "",
        "title": "",
        "projection": "",
        "strategic_actions": [],
        "indicator": "",
        "responsible_agencies": [],
        "axis_name": "",
        "axis_primary_color": "",
        "axis_secondary_color": "",
        "axis_phrases": [],
        "evolution": "",
        "monitoring": "",
        "measured_results": [],
        "regionalization": {
            "mode": "not_regionalizable",
            "note": None,
            "blocks": [],
        },
    }
