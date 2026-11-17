from typing import Any


META_FIELD_KEYS = [
    "number",
    "title",
    "title_highlight",
    "title_complement",
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
    "associated_works",
    "associated_projects",
    "extra_sections",
]


FIELD_LABELS = {
    "number": "Número da Meta",
    "title": "Título",
    "title_highlight": "Trecho destacado do título",
    "title_complement": "Complemento do título",
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
    "associated_works": "Obras associadas",
    "associated_projects": "Projetos associados",
    "extra_sections": "Seções extras",
}


def empty_meta_payload() -> dict[str, Any]:
    return {
        "number": "",
        "title": "",
        "title_highlight": "",
        "title_complement": "",
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
        "associated_works": [],
        "associated_projects": [],
        "extra_sections": [],
    }
