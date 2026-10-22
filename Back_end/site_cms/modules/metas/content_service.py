from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import (
    CmsMetaContent,
    CmsMetaVersion,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_meta_content(
    meta_code: str,
) -> CmsMetaContent | None:
    with rx.session() as session:
        return session.exec(
            select(CmsMetaContent).where(
                CmsMetaContent.meta_code
                == str(meta_code)
            )
        ).first()


def ensure_meta_content(
    *,
    meta_code: str,
    initial_content: dict[str, Any] | None = None,
    source: str = "legacy",
    smae_meta_id: int | None = None,
) -> tuple[CmsMetaContent, bool]:
    """
    Garante um registro editorial.

    Quando criado com conteúdo inicial, nasce publicado na versão 1.
    """

    with rx.session() as session:
        existing = session.exec(
            select(CmsMetaContent).where(
                CmsMetaContent.meta_code
                == str(meta_code)
            )
        ).first()

        if existing is not None:
            return existing, False

        now = _utc_now()
        content = deepcopy(
            initial_content or {}
        )

        source_map = {
            key: source
            for key, value in content.items()
            if value not in (
                None,
                "",
                [],
                {},
            )
        }

        meta = CmsMetaContent(
            meta_code=str(meta_code),
            smae_meta_id=smae_meta_id,
            status="published",
            draft_content=deepcopy(content),
            published_content=deepcopy(content),
            source_map=source_map,
            legacy_snapshot=(
                deepcopy(content)
                if source == "legacy"
                else {}
            ),
            legacy_imported_at=(
                now
                if source == "legacy"
                else None
            ),
            published_at=now,
        )

        session.add(meta)
        session.commit()
        session.refresh(meta)

        if meta.id is None:
            raise RuntimeError(
                "Não foi possível identificar o CMS da Meta criado."
            )

        version = CmsMetaVersion(
            meta_content_id=meta.id,
            version_number=1,
            content=deepcopy(content),
            source_map=deepcopy(
                source_map
            ),
            note=(
                "Conteúdo inicial importado da API antiga."
                if source == "legacy"
                else "Conteúdo inicial criado a partir do SMAE."
            ),
            published_at=now,
        )

        session.add(version)
        session.commit()

        return meta, True


def set_manual_field(
    *,
    meta_code: str,
    field_key: str,
    value: Any,
    actor_user_id: int | None,
) -> CmsMetaContent:
    """
    Altera um campo do draft e marca explicitamente sua origem como CMS.
    """

    with rx.session() as session:
        meta = session.exec(
            select(CmsMetaContent).where(
                CmsMetaContent.meta_code
                == str(meta_code)
            )
        ).first()

        if meta is None:
            raise ValueError(
                "Conteúdo editorial da Meta não encontrado."
            )

        draft = deepcopy(
            meta.draft_content or {}
        )
        sources = deepcopy(
            meta.source_map or {}
        )

        draft[field_key] = deepcopy(
            value
        )
        sources[field_key] = "cms"

        meta.draft_content = draft
        meta.source_map = sources
        meta.status = (
            "published"
            if draft == meta.published_content
            else "draft"
        )
        meta.updated_by = actor_user_id
        meta.updated_at = _utc_now()

        session.add(meta)
        session.commit()
        session.refresh(meta)

        return meta


def use_smae_field(
    *,
    meta_code: str,
    field_key: str,
    actor_user_id: int | None,
) -> CmsMetaContent:
    """Remove o override manual do campo e volta a acompanhar o SMAE."""

    with rx.session() as session:
        meta = session.exec(
            select(CmsMetaContent).where(
                CmsMetaContent.meta_code
                == str(meta_code)
            )
        ).first()

        if meta is None:
            raise ValueError(
                "Conteúdo editorial da Meta não encontrado."
            )

        snapshot = deepcopy(
            meta.smae_snapshot or {}
        )

        if field_key not in snapshot:
            raise ValueError(
                "O SMAE não possui valor disponível para este campo."
            )

        draft = deepcopy(
            meta.draft_content or {}
        )
        sources = deepcopy(
            meta.source_map or {}
        )

        draft[field_key] = deepcopy(
            snapshot[field_key]
        )
        sources[field_key] = "smae"

        meta.draft_content = draft
        meta.source_map = sources
        meta.status = (
            "published"
            if draft == meta.published_content
            else "draft"
        )
        meta.updated_by = actor_user_id
        meta.updated_at = _utc_now()

        session.add(meta)
        session.commit()
        session.refresh(meta)

        return meta


def publish_meta(
    *,
    meta_code: str,
    actor_user_id: int | None,
    note: str = "",
) -> tuple[CmsMetaContent, CmsMetaVersion]:
    """Publica o draft atual e cria uma versão imutável."""

    with rx.session() as session:
        meta = session.exec(
            select(CmsMetaContent).where(
                CmsMetaContent.meta_code
                == str(meta_code)
            )
        ).first()

        if meta is None or meta.id is None:
            raise ValueError(
                "Conteúdo editorial da Meta não encontrado."
            )

        versions = list(
            session.exec(
                select(CmsMetaVersion).where(
                    CmsMetaVersion.meta_content_id
                    == meta.id
                )
            ).all()
        )

        next_version = (
            max(
                (
                    version.version_number
                    for version in versions
                ),
                default=0,
            )
            + 1
        )

        now = _utc_now()

        meta.published_content = deepcopy(
            meta.draft_content or {}
        )
        meta.status = "published"
        meta.published_by = actor_user_id
        meta.published_at = now
        meta.updated_by = actor_user_id
        meta.updated_at = now

        version = CmsMetaVersion(
            meta_content_id=meta.id,
            version_number=next_version,
            content=deepcopy(
                meta.published_content
            ),
            source_map=deepcopy(
                meta.source_map or {}
            ),
            note=(
                note.strip()
                or "Conteúdo da Meta publicado pelo CMS."
            ),
            published_by=actor_user_id,
            published_at=now,
        )

        session.add(meta)
        session.add(version)
        session.commit()

        session.refresh(meta)
        session.refresh(version)

        return meta, version
