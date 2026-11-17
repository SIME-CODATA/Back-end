"""Persistência e regras de edição/publicação dos registros de monitoramento.

Nunca edita cms_meta_contents ou os snapshots SMAE já existentes.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import CmsMetaContent, CmsMetaGeoRecord, CmsMetaGeoVersion
from Back_end.site_cms.modules.metas.code import canonical_meta_code
from Back_end.site_cms.modules.metas.geografia.parser import COLUMNS, IDENTITY_FIELDS


def now():
    return datetime.now(timezone.utc)


def import_rows(rows: list[dict[str, Any]], *, dry_run: bool = True) -> dict[str, Any]:
    """Upsert por source_key: idempotente e não apaga overrides ou publicações.

    Falha inteiramente se encontrar meta inexistente, para não mascarar erros.
    """
    result = {"received": len(rows), "created": 0, "updated": 0,
              "unchanged": 0, "conflict_fields": 0, "dry_run": dry_run}
    with rx.session() as session:
        metas = set(session.exec(select(CmsMetaContent.meta_code)).all())
        missing = sorted({row["meta_code"] for row in rows} - metas)
        if missing:
            raise ValueError(f"Metas não cadastradas no CMS: {', '.join(missing)}")
        for row in rows:
            current = session.exec(select(CmsMetaGeoRecord).where(
                CmsMetaGeoRecord.source_key == row["source_key"]
            )).first()
            incoming = deepcopy(row["payload"])
            if current is None:
                result["created"] += 1
                session.add(CmsMetaGeoRecord(
                    meta_code=row["meta_code"], external_code=row["external_code"],
                    source=row["source"], source_key=row["source_key"],
                    sheet_row=row["sheet_row"], source_payload=deepcopy(incoming),
                    draft_payload=deepcopy(incoming),
                    source_map={key: row["source"] for key in incoming},
                    published_payload=None,
                ))
                continue
            if current.meta_code != row["meta_code"]:
                raise ValueError("Tentativa de mover a ação entre Metas: " + row["source_key"])
            if current.source_payload == incoming and current.is_active:
                result["unchanged"] += 1
                continue
            result["updated"] += 1
            prior = dict(current.source_payload or {})
            draft = deepcopy(current.draft_payload or {})
            sources = deepcopy(current.source_map or {})
            pending = deepcopy(current.pending_updates or {})
            for key in prior.keys() | incoming.keys():
                if prior.get(key) == incoming.get(key):
                    continue
                if sources.get(key) == "manual":
                    pending[key] = {
                        "anterior": prior.get(key, ""),
                        "recebido": incoming.get(key, ""),
                        "cms": draft.get(key, ""),
                    }
                    result["conflict_fields"] += 1
                else:
                    if key in incoming:
                        draft[key] = incoming[key]
                        sources[key] = row["source"]
                    else:
                        draft.pop(key, None)
                        sources.pop(key, None)
                    pending.pop(key, None)
            current.source_payload = incoming
            current.draft_payload = draft
            current.source_map = sources
            current.pending_updates = pending
            current.sheet_row = row["sheet_row"]
            current.is_active = True
            current.updated_at = now()
            current.imported_at = now()
            session.add(current)
        if dry_run:
            session.rollback()
        else:
            session.commit()
    return result


def list_rows(meta_code: str, *, limit: int = 300) -> list[CmsMetaGeoRecord]:
    code = canonical_meta_code(meta_code)
    with rx.session() as session:
        return list(session.exec(select(CmsMetaGeoRecord).where(
            CmsMetaGeoRecord.meta_code == code,
            CmsMetaGeoRecord.is_active == True,  # noqa: E712
        ).order_by(CmsMetaGeoRecord.id).limit(limit)).all())


def get_row(row_id: int, meta_code: str | None = None) -> CmsMetaGeoRecord | None:
    with rx.session() as session:
        row = session.get(CmsMetaGeoRecord, row_id)
        if row is not None and meta_code is not None and row.meta_code != canonical_meta_code(meta_code):
            return None
        return row


def create_manual(meta_code: str, *, actor_user_id: int | None) -> int:
    code = canonical_meta_code(meta_code)
    with rx.session() as session:
        meta = session.exec(select(CmsMetaContent).where(CmsMetaContent.meta_code == code)).first()
        if meta is None:
            raise ValueError("Meta não cadastrada no CMS.")
        unique = uuid4().hex[:12]
        fields = {col: "" for col in COLUMNS}
        fields["Meta"] = str(int(code))
        fields["codigo"] = f"CMS-{unique}"
        row = CmsMetaGeoRecord(
            meta_code=code, external_code=fields["codigo"], source="manual",
            source_key=f"manual:{code}:{unique}", source_payload={},
            draft_payload=fields, source_map={col: "manual" for col in fields},
            updated_by=actor_user_id,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return int(row.id)


def save_draft(row_id: int, changes: dict[str, str], *, actor_user_id: int | None) -> None:
    with rx.session() as session:
        row = session.get(CmsMetaGeoRecord, row_id)
        if row is None:
            raise ValueError("Registro não encontrado.")
        draft = deepcopy(row.draft_payload or {})
        sources = deepcopy(row.source_map or {})
        pending = deepcopy(row.pending_updates or {})
        for key, val in changes.items():
            if key in IDENTITY_FIELDS:
                raise ValueError("Meta e codigo são chaves de vínculo e não podem ser editados.")
            if key not in draft and key not in COLUMNS:
                raise ValueError(f"Campo não reconhecido: {key!r}")
            draft[key] = str(val)
            sources[key] = "manual"
            if key in pending:
                pending[key]["cms"] = str(val)
        row.draft_payload = draft
        row.source_map = sources
        row.pending_updates = pending
        row.updated_by = actor_user_id
        row.updated_at = now()
        session.add(row)
        session.commit()


def use_source(row_id: int, key: str, *, actor_user_id: int | None) -> None:
    with rx.session() as session:
        row = session.get(CmsMetaGeoRecord, row_id)
        if row is None or key in IDENTITY_FIELDS or key not in (row.source_payload or {}):
            raise ValueError("Campo sem valor original disponível.")
        draft = deepcopy(row.draft_payload or {})
        sources = deepcopy(row.source_map or {})
        pending = deepcopy(row.pending_updates or {})
        draft[key] = row.source_payload[key]
        sources[key] = row.source
        pending.pop(key, None)
        row.draft_payload, row.source_map, row.pending_updates = draft, sources, pending
        row.updated_by, row.updated_at = actor_user_id, now()
        session.add(row)
        session.commit()


def publish_row(row_id: int, *, actor_user_id: int | None, note: str = "") -> int:
    with rx.session() as session:
        row = session.get(CmsMetaGeoRecord, row_id)
        if row is None or not row.is_active:
            raise ValueError("Registro indisponível.")
        versions = list(session.exec(select(CmsMetaGeoVersion.version_number).where(
            CmsMetaGeoVersion.geo_record_id == row_id)).all())
        version_number = max(versions, default=0) + 1
        published = deepcopy(row.draft_payload or {})
        row.published_payload = published
        row.published_by, row.published_at = actor_user_id, now()
        session.add(row)
        session.add(CmsMetaGeoVersion(
            geo_record_id=row_id, version_number=version_number,
            content=published, source_map=deepcopy(row.source_map or {}),
            note=note[:500], published_by=actor_user_id, published_at=now(),
        ))
        session.commit()
        return version_number


def unpublish_row(row_id: int, *, actor_user_id: int | None) -> None:
    with rx.session() as session:
        row = session.get(CmsMetaGeoRecord, row_id)
        if row is None:
            raise ValueError("Registro não encontrado.")
        row.published_payload = None
        row.published_at = None
        row.updated_by, row.updated_at = actor_user_id, now()
        session.add(row)
        session.commit()
