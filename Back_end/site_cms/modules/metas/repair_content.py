from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import CmsMetaContent, CmsMetaVersion
from Back_end.site_cms.modules.metas.code import canonical_meta_code
from Back_end.site_cms.modules.metas.legacy_normalizer import normalize_legacy_meta


DEFAULT_LEGACY_SEARCH_URL = (
    "https://programademetas.prefeitura.sp.gov.br"
    "/backend/api/filtro_metas/search"
)


# Campos que o backend atual não sabe reconstruir com fidelidade a partir
# do SMAE. O site legado é usado somente como semente; depois disso o CMS
# pode personalizá-los normalmente.
LEGACY_AUTHORITATIVE_FIELDS = {
    "title_highlight",
    "title_complement",
    "projection",
    "strategic_actions",
    "indicator",
    "axis_primary_color",
    "axis_secondary_color",
    "axis_phrases",
    "evolution",
    "measured_results",
    "regionalization",
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _post_json(url: str, payload: dict[str, Any]) -> Any:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "PDM-V2-Meta-Repair/1.0",
        },
    )

    try:
        with urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(
            f"API antiga respondeu HTTP {error.code}: {url}"
        ) from error
    except URLError as error:
        raise RuntimeError(
            f"Não foi possível acessar a API antiga: {url}"
        ) from error


def _empty(value: Any) -> bool:
    return value in (None, "", [], {})


def _next_version(session, meta_id: int) -> int:
    versions = list(
        session.exec(
            select(CmsMetaVersion).where(
                CmsMetaVersion.meta_content_id == meta_id
            )
        ).all()
    )
    return max((item.version_number for item in versions), default=0) + 1


def repair_from_legacy(
    *,
    url: str,
    source_file: str = "",
    publish: bool,
    dry_run: bool,
) -> dict[str, Any]:
    if source_file:
        response = json.loads(
            Path(source_file).read_text(encoding="utf-8")
        )
    else:
        response = _post_json(url, {})
    raw_metas = response.get("metas") or []

    report = {
        "api_total": len(raw_metas),
        "created": 0,
        "repaired": 0,
        "unchanged": 0,
        "fields_filled": 0,
        "published": 0,
        "dry_run": dry_run,
    }

    with rx.session() as session:
        existing_rows = list(session.exec(select(CmsMetaContent)).all())
        by_code = {
            canonical_meta_code(row.meta_code): row
            for row in existing_rows
        }

        now = _utc_now()

        for raw_meta in raw_metas:
            legacy = normalize_legacy_meta(raw_meta)
            code = canonical_meta_code(legacy.get("number"))
            if not code:
                continue

            row = by_code.get(code)

            if row is None:
                report["created"] += 1
                report["fields_filled"] += sum(
                    1 for value in legacy.values() if not _empty(value)
                )

                if dry_run:
                    continue

                source_map = {
                    key: "legacy"
                    for key, value in legacy.items()
                    if not _empty(value)
                }
                row = CmsMetaContent(
                    meta_code=code,
                    status="published" if publish else "draft",
                    draft_content=deepcopy(legacy),
                    published_content=deepcopy(legacy) if publish else {},
                    source_map=source_map,
                    legacy_snapshot=deepcopy(legacy),
                    legacy_imported_at=now,
                    published_at=now if publish else None,
                )
                session.add(row)
                session.flush()
                by_code[code] = row

                if publish and row.id is not None:
                    session.add(
                        CmsMetaVersion(
                            meta_content_id=row.id,
                            version_number=1,
                            content=deepcopy(legacy),
                            source_map=deepcopy(source_map),
                            note="Ficha inicial reparada a partir do site legado.",
                            published_at=now,
                        )
                    )
                    report["published"] += 1
                continue

            draft = deepcopy(row.draft_content or {})
            published_content = deepcopy(row.published_content or {})
            sources = deepcopy(row.source_map or {})
            fields_filled = 0

            for key, legacy_value in legacy.items():
                if _empty(legacy_value):
                    continue

                current_source = sources.get(key)
                current_value = draft.get(key)

                # Nunca destrói personalização humana.
                if current_source == "cms":
                    continue

                # Alguns campos foram mapeados incorretamente para o SMAE em
                # versões anteriores (ex.: contexto -> projection). Para esses
                # campos, o legado atual é a semente confiável até existir um
                # mapeamento SMAE oficial validado.
                legacy_preferred = key in LEGACY_AUTHORITATIVE_FIELDS

                if (
                    legacy_preferred
                    or _empty(current_value)
                    or current_source in (None, "legacy")
                ):
                    if current_value != legacy_value or current_source != "legacy":
                        draft[key] = deepcopy(legacy_value)
                        sources[key] = "legacy"
                        fields_filled += 1

            if fields_filled == 0:
                report["unchanged"] += 1
                continue

            report["repaired"] += 1
            report["fields_filled"] += fields_filled

            if dry_run:
                continue

            row.draft_content = draft
            row.source_map = sources
            row.legacy_snapshot = deepcopy(legacy)
            row.legacy_imported_at = now
            row.updated_at = now

            if publish:
                row.published_content = deepcopy(draft)
                row.status = "published"
                row.published_at = now
                if row.id is not None:
                    session.add(
                        CmsMetaVersion(
                            meta_content_id=row.id,
                            version_number=_next_version(session, row.id),
                            content=deepcopy(draft),
                            source_map=deepcopy(sources),
                            note="Campos ausentes reparados a partir do site legado.",
                            published_at=now,
                        )
                    )
                    report["published"] += 1
            else:
                row.status = (
                    "published"
                    if draft == published_content
                    else "draft"
                )

            session.add(row)

        if not dry_run:
            session.commit()

    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preenche campos ausentes nas fichas CMS sem sobrescrever overrides."
    )
    parser.add_argument(
        "--url",
        default=os.getenv("LEGACY_META_SEARCH_URL", DEFAULT_LEGACY_SEARCH_URL),
    )
    parser.add_argument(
        "--file",
        default="",
        help=(
            "Arquivo JSON exportado da API antiga. Quando informado, "
            "não faz requisição HTTP."
        ),
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publica automaticamente somente os campos reparados.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra quantas fichas/campos seriam alterados sem gravar.",
    )
    args = parser.parse_args()

    report = repair_from_legacy(
        url=args.url,
        source_file=args.file,
        publish=args.publish,
        dry_run=args.dry_run,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
