"""Gestão em lote da origem editorial e publicação das Metas.

Não altera dados do SMAE, nem planilhas ou arquivos geográficos.
Todas as operações passam por validação prévia e uma transação SQL.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import CmsMetaContent, CmsMetaSyncConflict, CmsMetaVersion
from Back_end.site_cms.modules.metas.code import canonical_meta_code
from Back_end.site_cms.modules.metas.schema import META_FIELD_KEYS


def _present(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def _sources_for_latest_versions(versions: list[CmsMetaVersion]) -> dict[int, dict[str, str]]:
    latest: dict[int, CmsMetaVersion] = {}
    for version in versions:
        meta_id = version.meta_content_id
        if meta_id not in latest or (version.version_number, version.id or 0) > (
            latest[meta_id].version_number, latest[meta_id].id or 0
        ):
            latest[meta_id] = version
    return {meta_id: dict(version.source_map or {}) for meta_id, version in latest.items()}


def _needs_publication(meta: CmsMetaContent, published_sources: dict[str, str]) -> bool:
    draft = dict(meta.draft_content or {})
    published = dict(meta.published_content or {})
    if not published:
        return bool(draft)
    if draft != published:
        return True
    sources = dict(meta.source_map or {})
    return any(
        sources.get(key, "legacy") != published_sources.get(key, "legacy")
        for key in META_FIELD_KEYS
        if key in draft or key in published
    )


def _normalize_codes(codes: list[str]) -> list[str]:
    values = sorted({canonical_meta_code(value) for value in codes if str(value).strip()})
    if not values or len(values) > 200:
        raise ValueError("Selecione entre 1 e 200 metas para esta operação.")
    return values


def apply_bulk_operation(
    *, codes: list[str], action: str, field_key: str,
    actor_user_id: int | None, note: str = "",
) -> dict[str, Any]:
    """Muda a origem de UM campo em várias metas ou publica vários rascunhos.

    'cms' preserva o valor do rascunho e impede substituição automática pelo SMAE.
    'smae' copia o snapshot disponível para o rascunho (nunca publica sozinho).
    'publish' publica os drafts e captura a origem dos campos na versão histórica.
    Em caso de validação inválida para qualquer meta: nenhuma meta é alterada.
    """
    if action not in {"cms", "smae", "publish"}:
        raise ValueError("Ação inválida.")
    if action != "publish" and field_key not in META_FIELD_KEYS:
        raise ValueError("Campo não permitido para gestão de origem.")
    codes = _normalize_codes(codes)

    with rx.session() as session:
        metas = list(session.exec(select(CmsMetaContent).where(
            CmsMetaContent.meta_code.in_(codes)
        ).with_for_update()).all())
        by_code = {str(meta.meta_code): meta for meta in metas}
        absent = set(codes) - set(by_code)
        if absent:
            raise ValueError("Metas ausentes do CMS: " + ", ".join(sorted(absent)))

        ids = [int(meta.id) for meta in metas if meta.id is not None]
        if len(ids) != len(metas):
            raise ValueError("Uma ou mais metas não possuem identificador no banco.")
        pending = list(session.exec(select(CmsMetaSyncConflict).where(
            CmsMetaSyncConflict.meta_content_id.in_(ids),
            CmsMetaSyncConflict.status == "pending",
        )).all())
        conflicts_by_id: dict[int, set[str]] = {}
        for conflict in pending:
            conflicts_by_id.setdefault(int(conflict.meta_content_id), set()).add(str(conflict.field_key))

        versions = list(session.exec(select(CmsMetaVersion).where(
            CmsMetaVersion.meta_content_id.in_(ids)
        )).all())
        published_sources = _sources_for_latest_versions(versions)
        version_numbers: dict[int, int] = {}
        for version in versions:
            version_numbers[int(version.meta_content_id)] = max(
                version_numbers.get(int(version.meta_content_id), 0), version.version_number
            )

        plan: list[tuple[CmsMetaContent, dict[str, Any], dict[str, str]]] = []
        skipped: list[str] = []
        errors: list[str] = []

        for code in codes:
            meta = by_code[code]
            mid = int(meta.id)
            draft = deepcopy(dict(meta.draft_content or {}))
            sources = deepcopy(dict(meta.source_map or {}))
            if action == "publish":
                if conflicts_by_id.get(mid):
                    errors.append(f"{code}: possui conflitos SMAE pendentes")
                    continue
                if not _present(draft):
                    errors.append(f"{code}: rascunho sem conteúdo")
                    continue
                if not _needs_publication(meta, published_sources.get(mid, sources)):
                    skipped.append(code)
                    continue
            elif field_key in conflicts_by_id.get(mid, set()):
                errors.append(f"{code}: conflito pendente no campo selecionado")
                continue
            elif action == "cms":
                value = draft.get(field_key, (meta.published_content or {}).get(field_key))
                if not _present(value):
                    errors.append(f"{code}: campo sem valor para fixar no CMS")
                    continue
                if field_key not in draft:
                    draft[field_key] = deepcopy(value)
                if sources.get(field_key, "legacy") == "cms":
                    skipped.append(code)
                    continue
                sources[field_key] = "cms"
            else:
                snapshot = dict(meta.smae_snapshot or {})
                if field_key not in snapshot or not _present(snapshot[field_key]):
                    errors.append(f"{code}: sem valor SMAE disponível para este campo")
                    continue
                value = deepcopy(snapshot[field_key])
                if draft.get(field_key) == value and sources.get(field_key) == "smae":
                    skipped.append(code)
                    continue
                draft[field_key] = value
                sources[field_key] = "smae"
            plan.append((meta, draft, sources))

        if errors:
            raise ValueError("Nada foi alterado. " + "; ".join(errors[:8]) +
                             (f"; e mais {len(errors)-8} erro(s)" if len(errors) > 8 else ""))

        now = datetime.now(timezone.utc)
        changed: list[dict[str, Any]] = []
        for meta, draft, sources in plan:
            mid = int(meta.id)
            meta.updated_by = actor_user_id
            meta.updated_at = now
            if action == "publish":
                next_version = version_numbers.get(mid, 0) + 1
                meta.published_content = deepcopy(draft)
                meta.status = "published"
                meta.published_at = now
                meta.published_by = actor_user_id
                session.add(CmsMetaVersion(
                    meta_content_id=mid,
                    version_number=next_version,
                    content=deepcopy(draft),
                    source_map=deepcopy(sources),
                    note=note.strip() or "Publicação em lote pelo CMS.",
                    published_by=actor_user_id,
                    published_at=now,
                ))
                version_numbers[mid] = next_version
            else:
                meta.draft_content = draft
                meta.source_map = sources
                meta.status = (
                    "draft" if _needs_publication(meta, published_sources.get(mid, sources))
                    else "published"
                )
            session.add(meta)
            changed.append({"codigo": str(meta.meta_code), "id": mid})
        session.commit()
        return {"changed": changed, "skipped": skipped, "action": action, "field_key": field_key}
