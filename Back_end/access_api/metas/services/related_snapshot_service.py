from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_related_snapshot import (
    MetaRelatedSnapshot,
)
from Back_end.access_api.smae.services.meta_service import (
    fetch_relacionados_by_meta_ids,
)


@dataclass(frozen=True)
class RelatedSnapshotSyncResult:
    received: int
    created: int
    updated: int
    unchanged: int

REGIONS_BY_PARENT_ID = {
    181: "Zona Leste",
    182: "Zona Norte",
    183: "Zona Sul",
    184: "Zona Oeste",
    185: "Centro",
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _text(value: Any) -> str:
    return str(value or "").strip()


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _nested_name(value: Any, *keys: str) -> str:
    data = _dict(value)
    for key in keys:
        text = _text(data.get(key))
        if text:
            return text
    return ""


def _safe_float(value: Any) -> float | None:
    if value in (None, ""):
        return None

    if isinstance(value, bool):
        return None

    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def _valid_coordinates(
    latitude: float | None,
    longitude: float | None,
) -> tuple[float | None, float | None]:
    if latitude is None or longitude is None:
        return None, None

    if not (-90 <= latitude <= 90):
        return None, None

    if not (-180 <= longitude <= 180):
        return None, None

    return latitude, longitude


def _walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
        return

    if isinstance(value, list):
        for child in value:
            yield from _walk_dicts(child)


def extract_coordinates(value: Any) -> tuple[float | None, float | None]:
    """Busca coordenadas sem assumir uma única versão do payload do SMAE.

    O endpoint /meta/relacionados já mudou de forma ao longo do tempo. Em vez
    de descartar informação desconhecida, procuramos pares conhecidos em
    qualquer nível do objeto e preservamos o payload bruto no banco.
    """

    pairs = (
        ("latitude", "longitude"),
        ("lat", "lon"),
        ("lat", "lng"),
        ("lat", "longitude"),
        ("latitude", "lng"),
        ("y", "x"),
    )

    for data in _walk_dicts(value):
        lowered = {
            str(key).casefold(): item
            for key, item in data.items()
        }

        for lat_key, lon_key in pairs:
            if lat_key not in lowered or lon_key not in lowered:
                continue

            latitude = _safe_float(lowered.get(lat_key))
            longitude = _safe_float(lowered.get(lon_key))
            latitude, longitude = _valid_coordinates(
                latitude,
                longitude,
            )

            if latitude is not None and longitude is not None:
                return latitude, longitude

        coordinates = lowered.get("coordinates")
        if (
            isinstance(coordinates, (list, tuple))
            and len(coordinates) >= 2
        ):
            # GeoJSON utiliza [longitude, latitude].
            longitude = _safe_float(coordinates[0])
            latitude = _safe_float(coordinates[1])
            latitude, longitude = _valid_coordinates(
                latitude,
                longitude,
            )
            if latitude is not None and longitude is not None:
                return latitude, longitude

    return None, None


def _address_from(value: Any) -> str:
    """Extrai um endereço textual quando o SMAE o fornece."""

    direct_keys = (
        "endereco_completo",
        "endereco",
        "logradouro",
        "localizacao",
        "local",
    )

    for data in _walk_dicts(value):
        lowered = {
            str(key).casefold(): item
            for key, item in data.items()
        }

        for key in direct_keys:
            item = lowered.get(key)
            if isinstance(item, str) and item.strip():
                return item.strip()

            if isinstance(item, dict):
                parts = [
                    _text(item.get(part_key))
                    for part_key in (
                        "logradouro",
                        "numero",
                        "complemento",
                        "bairro",
                        "cep",
                    )
                ]
                parts = [part for part in parts if part]
                if parts:
                    return ", ".join(parts)

    return ""


def _subprefectures(raw: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []

    for item in _list(raw.get("subprefeituras")):
        if not isinstance(item, dict):
            continue

        result.append(
            {
                "id": item.get("id"),
                "name": _text(
                    item.get("descricao")
                    or item.get("nome")
                ),
                "parent_id": item.get("parente_id"),
            }
        )

    return result


def normalize_associated_work(raw: dict[str, Any]) -> dict[str, Any]:
    tipo = _dict(raw.get("tipo_intervencao"))
    equipamento = _dict(raw.get("equipamento"))
    subprefeituras = _subprefectures(raw)
    regions = sorted(
        {
            REGIONS_BY_PARENT_ID.get(int(item.get("parent_id")))
            for item in subprefeituras
            if item.get("parent_id") not in (None, "")
            and str(item.get("parent_id")).isdigit()
            and REGIONS_BY_PARENT_ID.get(int(item.get("parent_id")))
        },
        key=str.casefold,
    )
    latitude, longitude = extract_coordinates(raw)

    return {
        "id": raw.get("id"),
        "code": _text(raw.get("codigo")),
        "name": _text(raw.get("nome")),
        "intervention_type": _nested_name(
            tipo,
            "nome",
            "descricao",
        ),
        "subprefectures": subprefeituras,
        "regions": regions,
        "equipment": _nested_name(
            equipamento,
            "nome",
            "descricao",
        ),
        "status": _text(raw.get("status")),
        "percent_complete": raw.get("percentual_concluido"),
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "address": _address_from(raw),
        },
    }


def normalize_associated_project(raw: dict[str, Any]) -> dict[str, Any]:
    portfolio = _dict(raw.get("portfolio"))
    stage = _dict(raw.get("projeto_etapa"))
    latitude, longitude = extract_coordinates(raw)

    return {
        "id": raw.get("id"),
        "code": _text(raw.get("codigo")),
        "name": _text(raw.get("nome")),
        "portfolio": _nested_name(
            portfolio,
            "titulo",
            "nome",
            "descricao",
        ),
        "stage": _nested_name(
            stage,
            "descricao",
            "nome",
        ),
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "address": _address_from(raw),
        },
    }


def normalize_related_meta(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": raw.get("meta_id") or raw.get("id"),
        "code": _text(
            raw.get("meta_codigo")
            or raw.get("codigo")
        ),
        "title": _text(
            raw.get("meta_titulo")
            or raw.get("titulo")
        ),
    }


def normalize_related_payload(
    payload: dict[str, Any] | None,
) -> dict[str, Any]:
    payload = payload if isinstance(payload, dict) else {}

    works = [
        normalize_associated_work(item)
        for item in _list(payload.get("obras"))
        if isinstance(item, dict)
    ]

    projects = [
        normalize_associated_project(item)
        for item in _list(payload.get("projetos"))
        if isinstance(item, dict)
    ]

    related_metas = [
        normalize_related_meta(item)
        for item in _list(payload.get("metas"))
        if isinstance(item, dict)
    ]

    return {
        "works": works,
        "projects": projects,
        "related_metas": related_metas,
    }


def build_geo_features(
    *,
    meta_code: str,
    payload: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    normalized = normalize_related_payload(payload)
    features: list[dict[str, Any]] = []

    for source_type, items in (
        ("work", normalized["works"]),
        ("project", normalized["projects"]),
    ):
        for item in items:
            location = item.get("location") or {}
            latitude = location.get("latitude")
            longitude = location.get("longitude")

            geometry = None
            if latitude is not None and longitude is not None:
                geometry = {
                    "type": "Point",
                    "coordinates": [
                        longitude,
                        latitude,
                    ],
                }

            features.append(
                {
                    "type": "Feature",
                    "geometry": geometry,
                    "properties": {
                        "meta_code": meta_code,
                        "source_type": source_type,
                        "id": item.get("id"),
                        "code": item.get("code"),
                        "name": item.get("name"),
                        "status": item.get("status"),
                        "percent_complete": item.get(
                            "percent_complete"
                        ),
                        "address": location.get("address") or "",
                        "subprefectures": item.get(
                            "subprefectures",
                            [],
                        ),
                    },
                }
            )

    return features


def get_related_snapshot(
    *,
    meta_id: int | None = None,
    smae_meta_id: int | None = None,
) -> MetaRelatedSnapshot | None:
    if meta_id is None and smae_meta_id is None:
        raise ValueError("Informe meta_id ou smae_meta_id.")

    with rx.session() as session:
        query = select(MetaRelatedSnapshot)

        if meta_id is not None:
            query = query.where(
                MetaRelatedSnapshot.meta_id == meta_id
            )
        else:
            query = query.where(
                MetaRelatedSnapshot.smae_meta_id == smae_meta_id
            )

        row = session.exec(query).first()
        if row is not None:
            session.expunge(row)
        return row


def sync_related_snapshots() -> RelatedSnapshotSyncResult:
    """Sincroniza /meta/relacionados de todas as metas para PostgreSQL."""

    with rx.session() as session:
        metas = list(
            session.exec(
                select(Meta).order_by(Meta.smae_id)
            ).all()
        )

        identities = [
            (int(meta.id), int(meta.smae_id), str(meta.codigo))
            for meta in metas
            if meta.id is not None and meta.smae_id is not None
        ]

    related_by_smae = fetch_relacionados_by_meta_ids(
        [smae_id for _, smae_id, _ in identities]
    )

    created = 0
    updated = 0
    unchanged = 0
    now = _utc_now()

    with rx.session() as session:
        existing_rows = list(
            session.exec(
                select(MetaRelatedSnapshot)
            ).all()
        )
        by_meta_id = {
            int(row.meta_id): row
            for row in existing_rows
        }

        for meta_id, smae_id, meta_code in identities:
            raw_payload = related_by_smae.get(smae_id) or {
                "metas": [],
                "obras": [],
                "projetos": [],
            }

            geo_features = build_geo_features(
                meta_code=meta_code,
                payload=raw_payload,
            )

            existing = by_meta_id.get(meta_id)
            if existing is None:
                session.add(
                    MetaRelatedSnapshot(
                        meta_id=meta_id,
                        smae_meta_id=smae_id,
                        payload=deepcopy(raw_payload),
                        geo_features=deepcopy(geo_features),
                        synced_at=now,
                    )
                )
                created += 1
                continue

            if (
                (existing.payload or {}) == raw_payload
                and (existing.geo_features or []) == geo_features
                and int(existing.smae_meta_id) == smae_id
            ):
                unchanged += 1
                continue

            existing.smae_meta_id = smae_id
            existing.payload = deepcopy(raw_payload)
            existing.geo_features = deepcopy(geo_features)
            existing.synced_at = now
            session.add(existing)
            updated += 1

        session.commit()

    return RelatedSnapshotSyncResult(
        received=len(identities),
        created=created,
        updated=updated,
        unchanged=unchanged,
    )
