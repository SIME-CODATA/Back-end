from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import (
    CmsSection,
    CmsSectionVersion,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_section_by_id(
    section_id: int,
) -> CmsSection | None:
    with rx.session() as session:
        return session.get(
            CmsSection,
            section_id,
        )


def save_section_draft(
    *,
    section_id: int,
    content: dict[str, Any],
    actor_user_id: int,
) -> CmsSection:
    """Salva o conteúdo como rascunho sem alterar a versão publicada."""

    with rx.session() as session:
        section = session.get(
            CmsSection,
            section_id,
        )

        if section is None:
            raise ValueError(
                "A seção do CMS não foi encontrada."
            )

        now = _utc_now()

        section.draft_content = deepcopy(content)
        section.status = (
            "published"
            if section.draft_content
            == section.published_content
            else "draft"
        )
        section.updated_by = actor_user_id
        section.updated_at = now
        section.source_type = "cms"

        session.add(section)
        session.commit()
        session.refresh(section)

        return section


def publish_section(
    *,
    section_id: int,
    actor_user_id: int,
    note: str = "",
) -> tuple[CmsSection, CmsSectionVersion]:
    """Publica o rascunho atual e cria uma nova versão imutável."""

    with rx.session() as session:
        section = session.get(
            CmsSection,
            section_id,
        )

        if section is None:
            raise ValueError(
                "A seção do CMS não foi encontrada."
            )

        current_versions = list(
            session.exec(
                select(CmsSectionVersion).where(
                    CmsSectionVersion.section_id
                    == section_id
                )
            ).all()
        )

        next_version = (
            max(
                (
                    version.version_number
                    for version in current_versions
                ),
                default=0,
            )
            + 1
        )

        now = _utc_now()

        section.published_content = deepcopy(
            section.draft_content
        )
        section.status = "published"
        section.published_by = actor_user_id
        section.published_at = now
        section.updated_by = actor_user_id
        section.updated_at = now
        section.source_type = "cms"

        version = CmsSectionVersion(
            section_id=section_id,
            version_number=next_version,
            content=deepcopy(
                section.published_content
            ),
            note=(
                note.strip()
                or "Conteúdo publicado pelo CMS."
            ),
            published_by=actor_user_id,
            published_at=now,
        )

        session.add(section)
        session.add(version)
        session.commit()

        session.refresh(section)
        session.refresh(version)

        return section, version


def restore_version_to_draft(
    *,
    section_id: int,
    version_number: int,
    actor_user_id: int,
) -> CmsSection:
    """
    Restaura uma versão anterior para o rascunho.

    A restauração NÃO publica automaticamente. O usuário ainda
    precisa revisar e publicar.
    """

    with rx.session() as session:
        section = session.get(
            CmsSection,
            section_id,
        )

        if section is None:
            raise ValueError(
                "A seção do CMS não foi encontrada."
            )

        version = session.exec(
            select(CmsSectionVersion).where(
                CmsSectionVersion.section_id
                == section_id,
                CmsSectionVersion.version_number
                == version_number,
            )
        ).first()

        if version is None:
            raise ValueError(
                "A versão solicitada não foi encontrada."
            )

        now = _utc_now()

        section.draft_content = deepcopy(
            version.content
        )
        section.status = (
            "published"
            if section.draft_content
            == section.published_content
            else "draft"
        )
        section.updated_by = actor_user_id
        section.updated_at = now
        section.source_type = "cms"

        session.add(section)
        session.commit()
        session.refresh(section)

        return section
