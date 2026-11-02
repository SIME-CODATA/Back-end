from __future__ import annotations

import json
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_related_snapshot import MetaRelatedSnapshot
from Back_end.access_api.metas.services.related_snapshot_service import (
    extract_coordinates,
)


def _shape(value: Any, depth: int = 0) -> Any:
    if depth >= 4:
        if isinstance(value, dict):
            return {"__keys__": sorted(str(key) for key in value.keys())}
        if isinstance(value, list):
            return {"__list_size__": len(value)}
        return type(value).__name__

    if isinstance(value, dict):
        return {
            str(key): _shape(item, depth + 1)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [_shape(item, depth + 1) for item in value[:2]]

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    return type(value).__name__


def main() -> None:
    with rx.session() as session:
        rows = list(
            session.exec(
                select(MetaRelatedSnapshot, Meta)
                .join(Meta, Meta.id == MetaRelatedSnapshot.meta_id)
                .order_by(Meta.codigo)
            ).all()
        )

    for snapshot, meta in rows:
        payload = snapshot.payload or {}
        works = payload.get("obras") or []
        projects = payload.get("projetos") or []

        candidates = [
            ("obra", item)
            for item in works
            if isinstance(item, dict)
        ] + [
            ("projeto", item)
            for item in projects
            if isinstance(item, dict)
        ]

        if not candidates:
            continue

        print(f"\n=== META {meta.codigo} / SMAE {meta.smae_id} ===")
        print(f"snapshot sincronizado em: {snapshot.synced_at}")

        for kind, item in candidates[:3]:
            latitude, longitude = extract_coordinates(item)
            print(f"\n[{kind.upper()}]")
            print(f"coordenadas detectadas: {latitude}, {longitude}")
            print(
                json.dumps(
                    _shape(item),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        return

    print(
        "Nenhum snapshot com obra/projeto foi encontrado. "
        "Execute sync_related_cli primeiro."
    )


if __name__ == "__main__":
    main()
