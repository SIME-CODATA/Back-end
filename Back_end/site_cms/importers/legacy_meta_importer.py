from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import ( CmsMetaContent, CmsMetaVersion, )
from Back_end.site_cms.modules.metas.legacy_normalizer import (
    normalize_legacy_meta,
)


DEFAULT_LEGACY_SEARCH_URL = (
    "https://programademetas.prefeitura.sp.gov.br"
    "/backend/api/filtro_metas/search"
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _post_json(
    url: str,
    payload: dict[str, Any],
) -> Any:
    body = json.dumps(
        payload
    ).encode("utf-8")

    request = Request(
        url,
        data=body,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "PDM-Site-CMS-Meta-Importer/1.0",
        },
    )

    try:
        with urlopen(
            request,
            timeout=90,
        ) as response:
            return json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

    except HTTPError as error:
        raise RuntimeError(
            "A API antiga respondeu "
            f"HTTP {error.code}: {url}"
        ) from error

    except URLError as error:
        raise RuntimeError(
            "Não foi possível acessar "
            f"a API antiga: {url}"
        ) from error


def _import_one(
    raw_meta: dict[str, Any],
) -> tuple[str, bool]:
    content = normalize_legacy_meta(
        raw_meta
    )

    meta_code = str(
        content.get("number") or ""
    ).strip()

    if not meta_code:
        raise ValueError(
            "Meta legada sem número/código."
        )

    with rx.session() as session:
        existing = session.exec(
            select(CmsMetaContent).where(
                CmsMetaContent.meta_code
                == meta_code
            )
        ).first()

        if existing is not None:
            return meta_code, False

        now = _utc_now()

        source_map = {
            key: "legacy"
            for key, value
            in content.items()
            if value not in (
                None,
                "",
                [],
                {},
            )
        }

        meta = CmsMetaContent(
            meta_code=meta_code,
            status="published",
            draft_content=content,
            published_content=content,
            source_map=source_map,
            legacy_snapshot=content,
            legacy_imported_at=now,
            published_at=now,
        )

        session.add(meta)
        session.commit()
        session.refresh(meta)

        if meta.id is None:
            raise RuntimeError(
                "Não foi possível identificar "
                f"a Meta {meta_code} criada."
            )

        session.add(
            CmsMetaVersion(
                meta_content_id=meta.id,
                version_number=1,
                content=content,
                source_map=source_map,
                note=(
                    "Conteúdo inicial importado "
                    "da API antiga do site."
                ),
                published_at=now,
            )
        )

        session.commit()

        return meta_code, True


def import_legacy_metas(
    *,
    url: str,
) -> dict[str, Any]:
    print(
        "[CMS METAS] Buscando metas na API antiga..."
    )

    response = _post_json(
        url,
        {},
    )

    metas = response.get(
        "metas"
    ) or []

    imported: list[str] = []
    skipped: list[str] = []

    for raw_meta in metas:
        meta_code, created = _import_one(
            raw_meta
        )

        if created:
            imported.append(
                meta_code
            )
            print(
                f"[CMS METAS] Importada: {meta_code}"
            )
        else:
            skipped.append(
                meta_code
            )
            print(
                f"[CMS METAS] Ignorada: {meta_code}"
            )

    return {
        "total_api": response.get(
            "total",
            len(metas),
        ),
        "imported": imported,
        "skipped": skipped,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Importa as fichas atuais da API antiga "
            "para a camada editorial do novo CMS."
        )
    )

    parser.add_argument(
        "--url",
        default=os.getenv(
            "LEGACY_META_SEARCH_URL",
            DEFAULT_LEGACY_SEARCH_URL,
        ),
        help=(
            "Endpoint POST /filtro_metas/search "
            "da API antiga."
        ),
    )

    args = parser.parse_args()

    result = import_legacy_metas(
        url=args.url,
    )

    print(
        "\n=== Importação de Metas concluída ==="
    )
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
