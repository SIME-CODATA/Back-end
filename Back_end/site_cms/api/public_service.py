from __future__ import annotations

from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import (
    CmsMetaContent,
    CmsPage,
    CmsSection,
)
from Back_end.site_cms.modules.metas.code import (
    canonical_meta_code,
)
from Back_end.site_cms.modules.metas.overview_service import (
    get_effective_budget,
)


def _page_sections(
    page_key: str,
) -> dict[str, Any]:
    with rx.session() as session:
        page = session.exec(
            select(CmsPage).where(
                CmsPage.key == page_key,
                CmsPage.is_active == True,  # noqa: E712
            )
        ).first()

        if page is None or page.id is None:
            return {}

        sections = list(
            session.exec(
                select(CmsSection)
                .where(
                    CmsSection.page_id == page.id,
                    CmsSection.enabled == True,  # noqa: E712
                )
                .order_by(
                    CmsSection.position,
                    CmsSection.id,
                )
            ).all()
        )

    return {
        section.key: dict(
            section.published_content
            or {}
        )
        for section in sections
    }


def get_public_home() -> dict[str, Any]:
    return _page_sections(
        "home"
    )


def get_public_single_page(
    page_key: str,
    section_key: str,
) -> dict[str, Any] | None:
    sections = _page_sections(
        page_key
    )

    content = sections.get(
        section_key
    )

    if content is None:
        return None

    return content


def list_public_metas() -> list[dict[str, Any]]:
    with rx.session() as session:
        rows = list(
            session.exec(
                select(
                    CmsMetaContent
                )
            ).all()
        )

    result = []

    for row in rows:
        content = dict(
            row.published_content
            or {}
        )

        if not content:
            continue

        result.append({
            "codigo": row.meta_code,
            "titulo": str(
                content.get(
                    "title"
                )
                or ""
            ),
            "eixo": str(
                content.get(
                    "axis_name"
                )
                or ""
            ),
            "cor_eixo": str(
                content.get(
                    "axis_primary_color"
                )
                or ""
            ),
        })

    def sort_key(
        item: dict[str, Any],
    ):
        raw = str(
            item.get(
                "codigo"
            )
            or ""
        )

        try:
            return (
                0,
                int(raw),
            )
        except ValueError:
            return (
                1,
                raw.casefold(),
            )

    return sorted(
        result,
        key=sort_key,
    )


def get_public_meta(
    code: str,
) -> dict[str, Any] | None:
    normalized = (
        canonical_meta_code(
            code
        )
    )

    with rx.session() as session:
        row = session.exec(
            select(
                CmsMetaContent
            ).where(
                CmsMetaContent.meta_code
                == normalized
            )
        ).first()

    if (
        row is None
        or not row.published_content
    ):
        return None

    return {
        "codigo": row.meta_code,
        **dict(
            row.published_content
        ),
    }


def _order_sort_key(
    value: Any,
) -> tuple[int, int | str]:
    """
    Ordena '1', '2', '10' numericamente quando possível,
    mas preserva o valor original do CMS.
    """

    raw = str(
        value or ""
    ).strip()

    try:
        return (
            0,
            int(raw),
        )
    except ValueError:
        return (
            1,
            raw.casefold(),
        )


def _public_budget(
    content: dict[str, Any],
) -> dict[str, Any]:
    """
    Converte o formato interno do CMS para o contrato público
    consumido pelo frontend do site.
    """

    budget = get_effective_budget(
        content
    )

    return {
        "orcamento_total": (
            budget.get(
                "total_budget"
            )
            or 0
        ),
        "total_metas": (
            budget.get(
                "total_metas"
            )
            or 0
        ),
        "orcamentos_por_eixo": [
            {
                "nome": str(
                    item.get(
                        "name"
                    )
                    or ""
                ),
                "cor_principal": str(
                    item.get(
                        "color"
                    )
                    or ""
                ),
                "qtd_metas": (
                    item.get(
                        "meta_count"
                    )
                    or 0
                ),
                "orcamento": (
                    item.get(
                        "budget"
                    )
                    or 0
                ),
            }
            for item in (
                budget.get(
                    "axes"
                )
                or []
            )
        ],
    }


def _public_know_metas(
    content: dict[str, Any],
) -> dict[str, Any]:
    """
    Conheça Metas é editorial.

    Os campos são preservados como texto livre no CMS.
    A lista já sai ordenada pela posição informada pelo usuário.
    """

    know = (
        content.get(
            "know_metas"
        )
        or {}
    )

    items = [
        {
            "nome": str(
                item.get(
                    "name"
                )
                or ""
            ),
            "valor": str(
                item.get(
                    "value"
                )
                or ""
            ),
            "ordem": str(
                item.get(
                    "order"
                )
                or ""
            ),
        }
        for item in (
            know.get(
                "items"
            )
            or []
        )
    ]

    items.sort(
        key=lambda item: (
            _order_sort_key(
                item.get(
                    "ordem"
                )
            )
        )
    )

    return {
        "titulo": str(
            know.get(
                "title"
            )
            or ""
        ),
        "list_conheca_metas": items,
        "tipo": "list",
    }


def get_public_overview() -> dict[str, Any] | None:
    sections = _page_sections(
        "metas_overview"
    )

    content = sections.get(
        "overview"
    )

    if content is None:
        return None

    return {
        "orcamento_geral": (
            _public_budget(
                content
            )
        ),
        "conheca_metas": (
            _public_know_metas(
                content
            )
        ),
    }


def get_public_overview_budget() -> dict[str, Any] | None:
    sections = _page_sections(
        "metas_overview"
    )

    content = sections.get(
        "overview"
    )

    if content is None:
        return None

    return _public_budget(
        content
    )


def get_public_know_metas() -> dict[str, Any] | None:
    sections = _page_sections(
        "metas_overview"
    )

    content = sections.get(
        "overview"
    )

    if content is None:
        return None

    return _public_know_metas(
        content
    )
