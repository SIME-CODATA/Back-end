from collections import defaultdict
from typing import TypedDict

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import (
    CmsMetaContent,
    CmsMetaSyncConflict,
)


class CmsMetaListItem(TypedDict):
    codigo: str
    titulo: str
    eixo: str
    status: str
    conflitos: str
    origem_titulo: str
    url: str


def _sort_key(
    code: str,
) -> tuple[int, str]:
    raw = str(
        code or ""
    ).strip()

    try:
        return (
            int(raw),
            raw,
        )
    except ValueError:
        return (
            999999,
            raw.casefold(),
        )


def list_cms_metas() -> list[
    CmsMetaListItem
]:
    with rx.session() as session:
        metas = list(
            session.exec(
                select(
                    CmsMetaContent
                )
            ).all()
        )

        pending_rows = session.exec(
            select(
                CmsMetaSyncConflict.meta_content_id,
            ).where(
                CmsMetaSyncConflict.status
                == "pending"
            )
        ).all()

    pending_by_meta: dict[
        int,
        int,
    ] = defaultdict(int)

    for row in pending_rows:
        try:
            meta_content_id = int(
                row
            )
        except (
            TypeError,
            ValueError,
        ):
            try:
                meta_content_id = int(
                    row[0]
                )
            except Exception:
                continue

        pending_by_meta[
            meta_content_id
        ] += 1

    result: list[
        CmsMetaListItem
    ] = []

    for meta in metas:
        draft = dict(
            meta.draft_content
            or {}
        )
        published = dict(
            meta.published_content
            or {}
        )
        sources = dict(
            meta.source_map
            or {}
        )

        content = (
            draft
            if draft
            else published
        )

        conflict_count = (
            pending_by_meta.get(
                int(meta.id or 0),
                0,
            )
        )

        result.append({
            "codigo": str(
                meta.meta_code
            ),
            "titulo": str(
                content.get(
                    "title"
                )
                or "Sem título"
            ),
            "eixo": str(
                content.get(
                    "axis_name"
                )
                or "Sem eixo"
            ),
            "status": (
                "Rascunho"
                if (
                    meta.draft_content
                    != meta.published_content
                )
                else "Publicado"
            ),
            "conflitos": str(
                conflict_count
            ),
            "origem_titulo": str(
                sources.get(
                    "title"
                )
                or "legacy"
            ),
            "url": (
                "/admin/site/metas/"
                f"{meta.meta_code}"
            ),
        })

    return sorted(
        result,
        key=lambda item: (
            _sort_key(
                item["codigo"]
            )
        ),
    )
