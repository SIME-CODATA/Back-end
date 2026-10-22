from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from Back_end.site_cms.services.content_service import (
    ensure_page,
    import_initial_section,
)


DEFAULT_LEGACY_BASE_URL = (
    "https://programademetas.prefeitura.sp.gov.br/backend/api"
)


@dataclass(frozen=True)
class LegacySectionConfig:
    page_key: str
    page_title: str
    page_description: str
    key: str
    name: str
    section_type: str
    position: int
    endpoint: str
    transformer: Callable[[Any], dict[str, Any]]


def _media_reference(value: Any) -> dict[str, Any] | None:
    if value in (None, ""):
        return None

    return {
        "media_id": None,
        "legacy_source": value,
    }


def transform_about_pdm(data: dict[str, Any]) -> dict[str, Any]:
    letter = data.get("carta_prefeito") or {}

    return {
        "heading": {
            "title": data.get("titulo", ""),
            "subtitle": data.get("subtitulo", ""),
        },
        "body": data.get("paragrafo", ""),
        "media": {
            "image": _media_reference(
                data.get("link_img")
            ),
        },
        "documents": {
            "about_pdf": _media_reference(
                data.get("link_pdf_about")
            ),
        },
        "mayor_message": {
            "title": letter.get("titulo", ""),
            "author": letter.get("nome_prefeito", ""),
            "paragraphs": letter.get("paragrafos") or [],
        },
    }


def transform_news(data: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "items": [
            {
                "title": item.get("titulo", ""),
                "url": item.get("link", ""),
                "date": item.get("data", ""),
                "priority": item.get("prioridade", 0),
            }
            for item in data or []
        ],
    }


def transform_axes(data: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "items": [
            {
                "legacy_id": item.get("id"),
                "name": item.get("nome", ""),
                "title": item.get("titulo", ""),
                "theme": {
                    "primary_color": item.get("cor_principal", ""),
                },
                "media": {
                    "image": _media_reference(
                        item.get("imagem")
                    ),
                    "card_image": _media_reference(
                        item.get("imagem_card")
                    ),
                },
                "highlights": item.get("lista") or [],
                "paragraphs": item.get("texto") or [],
            }
            for item in data or []
        ],
    }


def transform_transparency(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": data.get("titulo", ""),
        "subtitle": data.get("subtitulo"),
        "cards": [
            {
                "title": item.get("subtitulo", ""),
                "text": item.get("paragrafo", ""),
                "order": item.get("ordem", 0),
                "button": {
                    "label": item.get("nome_btn", ""),
                    "url": item.get("link"),
                },
            }
            for item in data.get("recursos") or []
        ],
    }


def transform_history(data: dict[str, Any]) -> dict[str, Any]:
    """
    Normaliza o Histórico para o modelo enxuto do novo CMS.

    Cada card mantém somente:
    - id
    - ordem
    - imagem
    - cores
    - documentos
    """

    cards = []

    for card_index, item in enumerate(
        data.get("cards") or []
    ):
        cards.append({
            "id": str(
                item.get("id") or ""
            ),
            "order": card_index + 1,
            "media": {
                "image": _media_reference(
                    item.get("imagem")
                ),
            },
            "theme": {
                "primary_color": item.get(
                    "cor_principal",
                    "#1281AA",
                ),
                "button_color": item.get(
                    "cor_botao",
                    "#292561",
                ),
            },
            "documents": [
                {
                    "type": document.get(
                        "tipo",
                        "pdm",
                    ),
                    "name": document.get(
                        "nome",
                        "",
                    ),
                    "file": _media_reference(
                        document.get("url")
                    ),
                }
                for document in (
                    item.get("documentos")
                    or []
                )
            ],
        })

    return {
        "title": data.get("titulo", ""),
        "instruction": data.get("instrucao", ""),
        "body": data.get("paragrafo", ""),
        "cards": cards,
    }


def transform_regionalization(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": data.get("titulo", ""),
        "subtitle": data.get("subtitulo", ""),
        "instruction": data.get("instrucao", ""),
        "body": data.get("paragrafo", ""),
        "document": _media_reference(
            data.get("link_arquivo")
        ),
        "dashboard_url": data.get("link_dashboard", ""),
    }


def transform_about(data: dict[str, Any]) -> dict[str, Any]:
    banner = data.get("banner") or {}
    objectives = data.get("objetivos") or {}
    how = data.get("como_feito") or {}
    indicators = data.get("indicadores") or {}
    participation = data.get("participacao") or {}

    return {
        "banner": {
            "eyebrow": banner.get("supertitulo", ""),
            "title": banner.get("titulo", ""),
            "subtitle": banner.get("subtitulo", ""),
            "documents": [
                value
                for value in [
                    _media_reference(
                        banner.get("link_pdf")
                    ),
                    _media_reference(
                        banner.get("link_pdf2")
                    ),
                ]
                if value is not None
            ],
            "summary": {
                "what": banner.get("o_que", ""),
                "why": banner.get("por_que", ""),
                "for_whom": banner.get("para_quem", ""),
            },
        },
        "objectives": {
            "transparency": objectives.get("transparencia", ""),
            "systemic_view": objectives.get("visao_sistemica", ""),
            "optimization": objectives.get("otimizacao", ""),
            "execution": objectives.get("execucao", ""),
        },
        "how_it_was_made": {
            "text": how.get("texto", ""),
            "cards": [
                {
                    "number": card.get("numero", ""),
                    "title": card.get("titulo", ""),
                    "content": card.get("conteudo", ""),
                    "detail": card.get("detalhe", ""),
                }
                for card in how.get("cards") or []
            ],
        },
        "indicators": {
            "text": indicators.get("texto", ""),
            "subtitle": indicators.get("subtitulo", ""),
            "section_call": indicators.get("chamada_subsecao", ""),
            "section_content": indicators.get("conteudo_subsecao", ""),
        },
        "participation": {
            "text": participation.get("texto", ""),
            "hearings_content": participation.get(
                "conteudo_audiencias",
                "",
            ),
            "hearings_video": _media_reference(
                participation.get(
                    "link_video_audiencias"
                )
            ),
            "feedback_content": participation.get(
                "conteudo_devolutivas",
                "",
            ),
        },
    }


LEGACY_SECTIONS = [
    LegacySectionConfig(
        page_key="home",
        page_title="Página Inicial",
        page_description="Conteúdo editorial da Página Inicial.",
        key="about_pdm",
        name="Seção Carta do prefeito",
        section_type="about_pdm",
        position=10,
        endpoint="/secoes_pagina_inicial/about_pdm",
        transformer=transform_about_pdm,
    ),
    LegacySectionConfig(
        page_key="home",
        page_title="Página Inicial",
        page_description="Conteúdo editorial da Página Inicial.",
        key="news",
        name="Notícias",
        section_type="news",
        position=20,
        endpoint="/secoes_pagina_inicial/noticias",
        transformer=transform_news,
    ),
    LegacySectionConfig(
        page_key="home",
        page_title="Página Inicial",
        page_description="Conteúdo editorial da Página Inicial.",
        key="axes",
        name="Eixos",
        section_type="axes",
        position=30,
        endpoint="/secoes_pagina_inicial/eixos",
        transformer=transform_axes,
    ),
    LegacySectionConfig(
        page_key="transparency",
        page_title="Transparência e Monitoramento",
        page_description="Conteúdo da página de transparência.",
        key="transparency",
        name="Transparência e Monitoramento",
        section_type="transparency",
        position=10,
        endpoint="/secoes_pagina_inicial/transparencia",
        transformer=transform_transparency,
    ),
    LegacySectionConfig(
        page_key="history",
        page_title="Histórico",
        page_description="Conteúdo da página Histórico.",
        key="history",
        name="Histórico",
        section_type="history",
        position=10,
        endpoint="/secoes_pagina_inicial/historico",
        transformer=transform_history,
    ),
    LegacySectionConfig(
        page_key="regionalization",
        page_title="Regionalização",
        page_description="Conteúdo da página Regionalização.",
        key="regionalization",
        name="Regionalização",
        section_type="regionalization",
        position=10,
        endpoint="/secoes_pagina_inicial/regionalizacao",
        transformer=transform_regionalization,
    ),
    LegacySectionConfig(
        page_key="about",
        page_title="Sobre o PdM",
        page_description="Conteúdo institucional da página Sobre.",
        key="about",
        name="Sobre o PdM",
        section_type="about",
        position=10,
        endpoint="/secoes_pagina_inicial/sobre",
        transformer=transform_about,
    ),
]


def _fetch_json(url: str) -> Any:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "PDM-Site-CMS-Importer/2.0",
        },
    )

    try:
        with urlopen(
            request,
            timeout=30,
        ) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    except HTTPError as error:
        raise RuntimeError(
            f"API legada respondeu HTTP {error.code}: {url}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Não foi possível acessar a API legada: {url}"
        ) from error


def import_legacy_site(
    *,
    base_url: str,
    force: bool = False,
) -> dict[str, Any]:
    imported: list[str] = []
    skipped: list[str] = []

    for config in LEGACY_SECTIONS:
        page = ensure_page(
            key=config.page_key,
            title=config.page_title,
            description=config.page_description,
        )

        if page.id is None:
            raise RuntimeError(
                f"Não foi possível identificar a página '{config.page_key}'."
            )

        endpoint_url = (
            base_url.rstrip("/")
            + config.endpoint
        )

        print(
            f"[CMS] Buscando {config.page_key}/{config.key}: "
            f"{endpoint_url}"
        )

        raw_data = _fetch_json(
            endpoint_url
        )
        content = config.transformer(
            raw_data
        )

        _, was_imported = import_initial_section(
            page_id=page.id,
            key=config.key,
            name=config.name,
            section_type=config.section_type,
            position=config.position,
            content=content,
            source_endpoint=config.endpoint,
            force=force,
        )

        identity = (
            f"{config.page_key}/{config.key}"
        )

        if was_imported:
            imported.append(identity)
            print(
                f"[CMS] Importado: {identity}"
            )
        else:
            skipped.append(identity)
            print(
                f"[CMS] Ignorado (já existe): {identity}"
            )

    return {
        "imported": imported,
        "skipped": skipped,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Importa o conteúdo editorial da API legada "
            "para as páginas corretas do novo CMS."
        )
    )

    parser.add_argument(
        "--base-url",
        default=os.getenv(
            "LEGACY_SITE_API_URL",
            DEFAULT_LEGACY_BASE_URL,
        ),
        help="URL base da API antiga.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Reimporta apenas quando ainda não existe "
            "histórico editorial posterior à versão inicial."
        ),
    )

    args = parser.parse_args()

    result = import_legacy_site(
        base_url=args.base_url,
        force=args.force,
    )

    print("\n=== Importação concluída ===")
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
