"""Resumo das metas para a lista e para a central de gestão em lote."""
from collections import defaultdict
from typing import TypedDict

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import CmsMetaContent, CmsMetaSyncConflict, CmsMetaVersion
from Back_end.site_cms.modules.metas.schema import FIELD_LABELS, META_FIELD_KEYS
from Back_end.site_cms.modules.metas.bulk_service import _present, _sources_for_latest_versions, _needs_publication


class CmsMetaListItem(TypedDict):
    codigo: str
    titulo: str
    eixo: str
    status: str
    conflitos: str
    origem_titulo: str
    url: str
    selected: bool
    published_fields: str
    pending_fields: str
    cms_fields: str
    smae_fields: str
    field_status: str
    field_source: str
    field_published_source: str
    field_published_preview: str
    field_draft_preview: str
    field_smae_available: str


def _sort_key(code: str) -> tuple[int, str]:
    raw = str(code or "").strip()
    try:
        return (int(raw), raw)
    except ValueError:
        return (999999, raw.casefold())


def _preview(value) -> str:
    if not _present(value):
        return "Sem conteúdo"
    if isinstance(value, list):
        return f"{len(value)} item(ns)"
    if isinstance(value, dict):
        return "Objeto estruturado"
    return (str(value)[:100] + "…") if len(str(value)) > 100 else str(value)


def _origin(source: str) -> str:
    return {"cms": "CMS", "smae": "SMAE", "legacy": "API antiga"}.get(source, "API antiga")


def list_cms_metas(field_key: str = "title") -> list[CmsMetaListItem]:
    if field_key not in META_FIELD_KEYS:
        field_key = "title"
    with rx.session() as session:
        metas = list(session.exec(select(CmsMetaContent)).all())
        pending_rows = list(session.exec(select(CmsMetaSyncConflict.meta_content_id).where(
            CmsMetaSyncConflict.status == "pending"
        )).all())
        versions = list(session.exec(select(CmsMetaVersion)).all())

    pending_by_meta: dict[int, int] = defaultdict(int)
    for row in pending_rows:
        try:
            mid = int(row)
        except (TypeError, ValueError):
            try:
                mid = int(row[0])
            except (TypeError, ValueError, IndexError):
                continue
        pending_by_meta[mid] += 1
    pub_sources_by_meta = _sources_for_latest_versions(versions)
    result: list[CmsMetaListItem] = []

    for meta in metas:
        draft = dict(meta.draft_content or {})
        published = dict(meta.published_content or {})
        sources = dict(meta.source_map or {})
        public_sources = pub_sources_by_meta.get(int(meta.id or 0), sources)
        content = draft if draft else published
        pending = _needs_publication(meta, public_sources)
        if not published:
            status = "Não publicado"
        elif pending:
            status = "Rascunho pendente"
        else:
            status = "Publicado"
        public_count = sum(_present(published.get(key)) for key in META_FIELD_KEYS)
        pending_count = sum(
            draft.get(key) != published.get(key)
            or (sources.get(key, "legacy") != public_sources.get(key, "legacy"))
            for key in META_FIELD_KEYS if key in draft or key in published
        )
        cms_count = sum(sources.get(key) == "cms" for key in META_FIELD_KEYS if key in draft)
        smae_count = sum(sources.get(key) == "smae" for key in META_FIELD_KEYS if key in draft)
        published_value = published.get(field_key)
        draft_value = draft.get(field_key)
        has_pub_value = _present(published_value)
        has_draft_value = _present(draft_value)
        if not has_pub_value and not has_draft_value:
            field_status = "Sem conteúdo"
        elif (draft_value != published_value or sources.get(field_key, "legacy") != public_sources.get(field_key, "legacy")):
            field_status = "Pendente" if has_pub_value else "Não publicado"
        elif has_pub_value:
            field_status = "Publicado"
        else:
            field_status = "Não publicado"

        result.append({
            "codigo": str(meta.meta_code),
            "titulo": str(content.get("title") or "Sem título"),
            "eixo": str(content.get("axis_name") or "Sem eixo"),
            "status": status,
            "conflitos": str(pending_by_meta.get(int(meta.id or 0), 0)),
            "origem_titulo": str(sources.get("title") or "legacy"),
            "url": "/admin/site/metas/" + str(meta.meta_code),
            "selected": False,
            "published_fields": str(public_count),
            "pending_fields": str(pending_count),
            "cms_fields": str(cms_count),
            "smae_fields": str(smae_count),
            "field_status": field_status,
            "field_source": _origin(sources.get(field_key, "legacy")),
            "field_published_source": _origin(public_sources.get(field_key, "legacy")) if has_pub_value else "Não publicado",
            "field_published_preview": _preview(published_value),
            "field_draft_preview": _preview(draft_value),
            "field_smae_available": "Sim" if _present((meta.smae_snapshot or {}).get(field_key)) else "Não",
        })
    return sorted(result, key=lambda item: _sort_key(item["codigo"]))
