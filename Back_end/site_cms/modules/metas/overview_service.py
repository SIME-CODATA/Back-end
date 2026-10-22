from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orcamento import (
    MetaOrcamento,
)
from Back_end.site_cms.models import (
    CmsPage,
    CmsSection,
)
from Back_end.site_cms.modules.metas.overview_seed import (
    legacy_overview_content,
)
from Back_end.site_cms.services.content_service import (
    ensure_page,
    import_initial_section,
)


OVERVIEW_PAGE_KEY = "metas_overview"
OVERVIEW_PAGE_TITLE = "Visão Geral das Metas"

OVERVIEW_SECTION_KEY = "overview"
OVERVIEW_SECTION_NAME = "Orçamento e Conheça Metas"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _decimal_to_number(
    value: Decimal | int | float | None,
) -> float:
    return float(
        value or Decimal("0")
    )


def _axis_color_map() -> dict[str, str]:
    """
    Obtém as cores já publicadas no CMS de Eixos.
    """

    with rx.session() as session:
        home = session.exec(
            select(CmsPage).where(
                CmsPage.key == "home"
            )
        ).first()

        if home is None or home.id is None:
            return {}

        axes = session.exec(
            select(CmsSection).where(
                CmsSection.page_id == home.id,
                CmsSection.key == "axes",
            )
        ).first()

        if axes is None:
            return {}

        content = dict(
            axes.published_content
            or axes.draft_content
            or {}
        )

    result: dict[str, str] = {}

    for item in content.get("items") or []:
        name = str(
            item.get("name")
            or item.get("title")
            or ""
        ).strip()

        theme = item.get("theme") or {}

        color = str(
            theme.get("primary_color")
            or ""
        ).strip()

        if name and color:
            result[
                name.casefold()
            ] = color

    return result


def calculate_budget_from_local_smae() -> dict[str, Any]:
    """
    Consolida o orçamento diretamente das tabelas locais do SMAE.

    O orçamento geral usa total_previsao.

    has_budget_data só fica True quando existe ao menos uma Meta
    com previsão maior que zero. Isso impede um snapshot financeiro
    ainda vazio de substituir a carga inicial da API antiga.
    """

    colors = _axis_color_map()

    with rx.session() as session:
        rows = session.exec(
            select(
                Meta.id,
                Meta.tema_descricao,
                MetaOrcamento.total_previsao,
            )
            .join(
                MetaOrcamento,
                MetaOrcamento.meta_id == Meta.id,
                isouter=True,
            )
        ).all()

    zero = Decimal("0")
    total_budget = zero

    axis_data: dict[
        str,
        dict[str, Any],
    ] = {}

    seen_meta_ids: set[int] = set()
    budget_rows = 0
    positive_budget_rows = 0

    for (
        meta_id,
        axis_name,
        total_previsao,
    ) in rows:
        meta_id = int(meta_id)
        seen_meta_ids.add(meta_id)

        if total_previsao is not None:
            budget_rows += 1

        budget = (
            total_previsao
            if total_previsao is not None
            else zero
        )

        if budget > zero:
            positive_budget_rows += 1

        total_budget += budget

        normalized_axis = str(
            axis_name
            or "Eixo não informado"
        ).strip()

        item = axis_data.setdefault(
            normalized_axis,
            {
                "name": normalized_axis,
                "color": (
                    colors.get(
                        normalized_axis.casefold()
                    )
                    or ""
                ),
                "meta_count": 0,
                "budget": zero,
            },
        )

        item["meta_count"] += 1
        item["budget"] += budget

    axes = [
        {
            "name": item["name"],
            "color": item["color"],
            "meta_count": int(
                item["meta_count"]
            ),
            "budget": _decimal_to_number(
                item["budget"]
            ),
        }
        for _, item in sorted(
            axis_data.items(),
            key=lambda pair: pair[0].casefold(),
        )
    ]

    return {
        "total_budget": _decimal_to_number(
            total_budget
        ),
        "total_metas": len(
            seen_meta_ids
        ),
        "axes": axes,
        "source": "smae",
        "updated_at": _utc_now().isoformat(),
        "has_budget_data": (
            positive_budget_rows > 0
        ),
        "budget_rows": budget_rows,
        "positive_budget_rows": positive_budget_rows,
    }


def _initial_overview_content() -> dict[str, Any]:
    """
    Começa com a carga da API antiga.

    Se já houver orçamento SMAE válido no banco local, ele passa a ser
    a origem automática imediatamente.
    """

    content = legacy_overview_content()

    local_budget = (
        calculate_budget_from_local_smae()
    )

    if local_budget.get(
        "has_budget_data"
    ):
        content["budget"][
            "source"
        ] = "smae"

        content["budget"][
            "smae_value"
        ] = deepcopy(
            local_budget
        )

    return content


def ensure_overview_section(
    *,
    initial_know_metas: dict[str, Any] | None = None,
) -> CmsSection:
    page = ensure_page(
        key=OVERVIEW_PAGE_KEY,
        title=OVERVIEW_PAGE_TITLE,
        description=(
            "Orçamento geral e indicadores editoriais "
            "da visão geral das Metas."
        ),
    )

    if page.id is None:
        raise RuntimeError(
            "Não foi possível identificar a página da Visão Geral."
        )

    with rx.session() as session:
        existing = session.exec(
            select(CmsSection).where(
                CmsSection.page_id == page.id,
                CmsSection.key == OVERVIEW_SECTION_KEY,
            )
        ).first()

        if existing is not None:
            return existing

    content = _initial_overview_content()

    if initial_know_metas:
        content[
            "know_metas"
        ] = deepcopy(
            initial_know_metas
        )

    section, _ = import_initial_section(
        page_id=page.id,
        key=OVERVIEW_SECTION_KEY,
        name=OVERVIEW_SECTION_NAME,
        section_type="metas_overview",
        position=10,
        content=content,
        source_endpoint=(
            "/visao_geral/orcamento_geral;"
            "/visao_geral/conheca_metas"
        ),
        force=False,
    )

    return section


def get_overview_section() -> CmsSection | None:
    with rx.session() as session:
        page = session.exec(
            select(CmsPage).where(
                CmsPage.key == OVERVIEW_PAGE_KEY
            )
        ).first()

        if page is None or page.id is None:
            return None

        return session.exec(
            select(CmsSection).where(
                CmsSection.page_id == page.id,
                CmsSection.key == OVERVIEW_SECTION_KEY,
            )
        ).first()


def get_effective_budget(
    content: dict[str, Any],
) -> dict[str, Any]:
    budget = content.get("budget") or {}

    source = str(
        budget.get("source")
        or "legacy"
    )

    if (
        source == "cms"
        and isinstance(
            budget.get("cms_value"),
            dict,
        )
    ):
        return deepcopy(
            budget["cms_value"]
        )

    if (
        source == "smae"
        and isinstance(
            budget.get("smae_value"),
            dict,
        )
        and budget.get(
            "smae_value"
        )
    ):
        return deepcopy(
            budget["smae_value"]
        )

    if isinstance(
        budget.get("legacy_value"),
        dict,
    ):
        return deepcopy(
            budget["legacy_value"]
        )

    return deepcopy(
        budget.get("smae_value")
        or {}
    )


def refresh_overview_budget_from_local() -> dict[str, Any]:
    """
    Atualiza o snapshot SMAE do orçamento no draft.

    Regras:
    - Snapshot financeiro zerado NÃO substitui o legado.
    - Override CMS nunca é sobrescrito.
    - Quando existe orçamento SMAE válido:
        legacy -> smae no draft
        smae -> atualiza smae no draft
        cms -> preserva cms e sinaliza update_available
    - published_content nunca é alterado automaticamente.
    """

    section = get_overview_section()

    if section is None or section.id is None:
        return {
            "updated": False,
            "reason": "overview_not_initialized",
        }

    new_budget = (
        calculate_budget_from_local_smae()
    )

    if not new_budget.get(
        "has_budget_data"
    ):
        return {
            "updated": False,
            "reason": "smae_budget_not_available",
            "budget_rows": new_budget.get(
                "budget_rows",
                0,
            ),
            "positive_budget_rows": (
                new_budget.get(
                    "positive_budget_rows",
                    0,
                )
            ),
        }

    with rx.session() as session:
        current = session.get(
            CmsSection,
            section.id,
        )

        if current is None:
            return {
                "updated": False,
                "reason": "overview_not_found",
            }

        draft = deepcopy(
            current.draft_content
            or {}
        )

        budget = deepcopy(
            draft.get("budget")
            or {}
        )

        previous_smae = deepcopy(
            budget.get("smae_value")
            or {}
        )

        source = str(
            budget.get("source")
            or "legacy"
        )

        changed = (
            previous_smae
            != new_budget
        )

        budget["smae_value"] = deepcopy(
            new_budget
        )

        if source == "cms":
            budget[
                "update_available"
            ] = changed

        else:
            budget["source"] = "smae"
            budget["cms_value"] = None
            budget[
                "update_available"
            ] = False

        draft["budget"] = budget

        current.draft_content = draft
        current.status = (
            "published"
            if current.draft_content
            == current.published_content
            else "draft"
        )
        current.updated_at = _utc_now()

        session.add(current)
        session.commit()

        return {
            "updated": True,
            "changed": changed,
            "source_before": source,
            "source_after": (
                budget.get("source")
            ),
            "update_available": bool(
                budget.get(
                    "update_available"
                )
            ),
        }
