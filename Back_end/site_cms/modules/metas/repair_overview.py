from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import (
    CmsSection,
    CmsSectionVersion,
)
from Back_end.site_cms.modules.metas.overview_seed import (
    legacy_overview_content,
)
from Back_end.site_cms.modules.metas.overview_service import (
    calculate_budget_from_local_smae,
    ensure_overview_section,
    get_effective_budget,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _is_empty_overview(
    content: dict,
) -> bool:
    know = (
        content.get(
            "know_metas"
        )
        or {}
    )

    items = (
        know.get(
            "items"
        )
        or []
    )

    budget = get_effective_budget(
        content
    )

    total_budget = float(
        budget.get(
            "total_budget"
        )
        or 0
    )

    axes = (
        budget.get(
            "axes"
        )
        or []
    )

    return (
        len(items) == 0
        and total_budget == 0
        and len(axes) == 0
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Repara a Visão Geral que foi criada vazia "
            "durante a primeira implementação."
        )
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Sobrescreve mesmo se a seção já possuir conteúdo."
        ),
    )

    args = parser.parse_args()

    section = ensure_overview_section()

    if section.id is None:
        raise RuntimeError(
            "Seção da Visão Geral sem ID."
        )

    with rx.session() as session:
        current = session.get(
            CmsSection,
            section.id,
        )

        if current is None:
            raise RuntimeError(
                "Seção da Visão Geral não encontrada."
            )

        existing_content = dict(
            current.draft_content
            or current.published_content
            or {}
        )

        if (
            not args.force
            and not _is_empty_overview(
                existing_content
            )
        ):
            print(
                "[CMS VISÃO GERAL] A seção já possui conteúdo. "
                "Nada foi alterado."
            )
            print(
                "Use --force somente se realmente quiser "
                "reaplicar a carga inicial."
            )
            return

        content = (
            legacy_overview_content()
        )

        local_budget = (
            calculate_budget_from_local_smae()
        )

        if local_budget.get(
            "has_budget_data"
        ):
            content[
                "budget"
            ][
                "source"
            ] = "smae"

            content[
                "budget"
            ][
                "smae_value"
            ] = deepcopy(
                local_budget
            )

            selected_source = (
                "smae"
            )
        else:
            # Guarda o diagnóstico, mas preserva o valor legado.
            content[
                "budget"
            ][
                "smae_value"
            ] = deepcopy(
                local_budget
            )

            selected_source = (
                "legacy"
            )

        now = _utc_now()

        current.draft_content = (
            deepcopy(
                content
            )
        )
        current.published_content = (
            deepcopy(
                content
            )
        )
        current.status = "published"
        current.enabled = True
        current.source_type = (
            "legacy_api"
        )
        current.source_endpoint = (
            "/visao_geral/orcamento_geral;"
            "/visao_geral/conheca_metas"
        )
        current.legacy_imported_at = now
        current.published_at = now
        current.updated_at = now

        session.add(current)
        session.flush()

        versions = list(
            session.exec(
                select(
                    CmsSectionVersion
                ).where(
                    CmsSectionVersion.section_id
                    == current.id
                )
            ).all()
        )

        next_version = (
            max(
                (
                    item.version_number
                    for item in versions
                ),
                default=0,
            )
            + 1
        )

        session.add(
            CmsSectionVersion(
                section_id=current.id,
                version_number=next_version,
                content=deepcopy(
                    content
                ),
                note=(
                    "Reparo da carga inicial da Visão Geral: "
                    "Orçamento Geral + Conheça Metas."
                ),
                published_at=now,
            )
        )

        session.commit()

    print(
        "\n=== Visão Geral reparada ==="
    )
    print(
        json.dumps(
            {
                "section_id": section.id,
                "budget_source": selected_source,
                "legacy_total_budget": 48841200000,
                "know_metas_cards": 5,
                "smae_has_budget_data": bool(
                    local_budget.get(
                        "has_budget_data"
                    )
                ),
                "smae_total_budget": (
                    local_budget.get(
                        "total_budget"
                    )
                ),
                "smae_budget_rows": (
                    local_budget.get(
                        "budget_rows"
                    )
                ),
                "smae_positive_budget_rows": (
                    local_budget.get(
                        "positive_budget_rows"
                    )
                ),
                "version_created": next_version,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
