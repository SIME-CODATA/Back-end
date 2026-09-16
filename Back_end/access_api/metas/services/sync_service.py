from dataclasses import dataclass

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta, utc_now
from Back_end.access_api.smae.services.meta_service import fetch_metas


@dataclass(frozen=True)
class MetaSyncResult:
    """Resultado de uma sincronização de metas com o SMAE."""

    received: int
    inserted: int
    updated: int
    unchanged: int


def _normalize_meta(raw_meta: dict) -> dict:
    """Transforma uma Meta recebida do SMAE no formato usado localmente."""

    smae_id = raw_meta.get("id")
    pdm_id = raw_meta.get("pdm_id")
    codigo = raw_meta.get("codigo")
    titulo = raw_meta.get("titulo")

    if smae_id is None:
        raise RuntimeError("Meta recebida do SMAE sem id.")

    if pdm_id is None:
        raise RuntimeError(
            f"Meta SMAE {smae_id} recebida sem pdm_id."
        )

    if not codigo:
        raise RuntimeError(
            f"Meta SMAE {smae_id} recebida sem código."
        )

    if not titulo:
        raise RuntimeError(
            f"Meta SMAE {smae_id} recebida sem título."
        )

    tema = raw_meta.get("tema") or {}

    return {
        "smae_id": smae_id,
        "pdm_id": pdm_id,
        "codigo": codigo,
        "titulo": titulo,
        "contexto": raw_meta.get("contexto"),
        "complemento": raw_meta.get("complemento"),
        "ativo": bool(raw_meta.get("ativo", False)),
        "tema_smae_id": tema.get("id"),
        "tema_descricao": tema.get("descricao"),
    }


def sync_metas() -> MetaSyncResult:
    """Sincroniza as metas do SMAE com o PostgreSQL local."""

    raw_metas = fetch_metas()

    normalized_metas = [
        _normalize_meta(raw_meta)
        for raw_meta in raw_metas
    ]

    incoming_ids = [
        meta["smae_id"]
        for meta in normalized_metas
    ]

    inserted = 0
    updated = 0
    unchanged = 0

    now = utc_now()

    with rx.session() as session:
        existing_metas = []

        if incoming_ids:
            existing_metas = session.exec(
                select(Meta).where(
                    Meta.smae_id.in_(incoming_ids)
                )
            ).all()

        existing_by_smae_id = {
            meta.smae_id: meta
            for meta in existing_metas
        }

        for meta_data in normalized_metas:
            smae_id = meta_data["smae_id"]

            existing_meta = existing_by_smae_id.get(smae_id)

            if existing_meta is None:
                meta = Meta(
                    **meta_data,
                    created_at=now,
                    updated_at=now,
                    synced_at=now,
                )

                session.add(meta)

                inserted += 1
                continue

            changed = False

            for field, value in meta_data.items():
                if field == "smae_id":
                    continue

                current_value = getattr(existing_meta, field)

                if current_value != value:
                    setattr(existing_meta, field, value)
                    changed = True

            if changed:
                existing_meta.updated_at = now
                updated += 1
            else:
                unchanged += 1

            existing_meta.synced_at = now

            session.add(existing_meta)

        session.commit()

    return MetaSyncResult(
        received=len(normalized_metas),
        inserted=inserted,
        updated=updated,
        unchanged=unchanged,
    )