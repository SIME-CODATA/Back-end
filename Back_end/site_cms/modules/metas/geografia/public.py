"""API de acesso público, com filtro de publicação em DOIS níveis."""
from sqlmodel import select
import reflex as rx

from Back_end.site_cms.models import CmsMetaContent, CmsMetaGeoRecord
from Back_end.site_cms.modules.metas.code import canonical_meta_code
from Back_end.site_cms.modules.metas.geografia.parser import PUBLIC_FLAG, safe_public_payload


def get_public_geo(meta_code: str) -> dict | None:
    code = canonical_meta_code(meta_code)
    with rx.session() as session:
        meta = session.exec(select(CmsMetaContent).where(CmsMetaContent.meta_code == code)).first()
        if meta is None or not meta.published_content:
            return None
        rows = list(session.exec(select(CmsMetaGeoRecord).where(
            CmsMetaGeoRecord.meta_code == code,
            CmsMetaGeoRecord.is_active == True,  # noqa: E712
            CmsMetaGeoRecord.published_payload.isnot(None),
        ).order_by(CmsMetaGeoRecord.id)).all())
    public_rows = []
    for item in rows:
        current = item.published_payload or {}
        # Mesmo que o editor altere a flag para "Sim", a fonte não publicada
        # continua privada até passar por um fluxo de autorização específico.
        source = item.source_payload or {}
        if str(current.get(PUBLIC_FLAG, "")).strip().casefold() != "sim":
            continue
        if item.source != "manual" and str(source.get(PUBLIC_FLAG, "")).strip().casefold() != "sim":
            continue
        public_rows.append(safe_public_payload(current))
    return {"codigo": code, "total": len(public_rows), "localizacoes": public_rows}
