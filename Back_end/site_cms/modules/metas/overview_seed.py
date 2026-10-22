from copy import deepcopy
from typing import Any


LEGACY_BUDGET: dict[str, Any] = {
    "total_budget": 48841200000,
    "total_metas": 132,
    "axes": [
        {
            "name": "Universo SP",
            "color": "#3DB54A",
            "meta_count": 54,
            "budget": 31700000000,
        },
        {
            "name": "Viver São Paulo",
            "color": "#F16622",
            "meta_count": 41,
            "budget": 16500000000,
        },
        {
            "name": "Cidade Empreendedora",
            "color": "#0000AB",
            "meta_count": 17,
            "budget": 346800000,
        },
        {
            "name": "Capital do Futuro",
            "color": "#792D49",
            "meta_count": 20,
            "budget": 294400000,
        },
    ],
    "source": "legacy",
}


LEGACY_KNOW_METAS: dict[str, Any] = {
    "title": "CONHECA METAS",
    "items": [
        {
            "name": "Metas atingidas",
            "value": "19",
            "order": "1",
        },
        {
            "name": "Metas com 50% ou mais de execução",
            "value": "49",
            "order": "2",
        },
        {
            "name": "123 metas em progresso e/ou atingidas",
            "value": "93%",
            "order": "3",
        },
        {
            "name": "Execução total do PdM",
            "value": "38,9%",
            "order": "4",
        },
        {
            "name": "Recursos Empenhados",
            "value": "12.4",
            "order": "5",
        },
    ],
}


def legacy_overview_content() -> dict[str, Any]:
    """
    Conteúdo inicial migrado da API antiga.

    O orçamento é mantido como fallback até que exista um snapshot
    financeiro válido vindo das tabelas locais sincronizadas do SMAE.
    """

    return {
        "budget": {
            "source": "legacy",
            "legacy_value": deepcopy(
                LEGACY_BUDGET
            ),
            "smae_value": {},
            "cms_value": None,
            "update_available": False,
        },
        "know_metas": deepcopy(
            LEGACY_KNOW_METAS
        ),
    }
