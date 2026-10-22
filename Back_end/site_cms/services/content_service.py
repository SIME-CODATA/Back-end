from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import (
    CmsPage,
    CmsSection,
    CmsSectionVersion,
)
from Back_end.site_cms.schemas.home.constants import (
    HOME_PAGE_KEY,
    HOME_PAGE_TITLE,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_page(
    *,
    key: str,
    title: str,
    description: str = "",
) -> CmsPage:
    """Garante a existência de uma página do CMS."""

    with rx.session() as session:
        page = session.exec(
            select(CmsPage).where(
                CmsPage.key == key
            )
        ).first()

        if page is not None:
            changed = False

            if page.title != title:
                page.title = title
                changed = True

            if description and page.description != description:
                page.description = description
                changed = True

            if changed:
                page.updated_at = _utc_now()
                session.add(page)
                session.commit()
                session.refresh(page)

            return page

        page = CmsPage(
            key=key,
            title=title,
            description=description,
        )

        session.add(page)
        session.commit()
        session.refresh(page)

        return page


def ensure_home_page() -> CmsPage:
    return ensure_page(
        key=HOME_PAGE_KEY,
        title=HOME_PAGE_TITLE,
        description=(
            "Conteúdo administrável da página inicial "
            "do site público do Programa de Metas."
        ),
    )


def import_initial_section(
    *,
    page_id: int,
    key: str,
    name: str,
    section_type: str,
    position: int,
    content: dict[str, Any],
    source_endpoint: str,
    force: bool = False,
) -> tuple[CmsSection, bool]:
    """
    Importa a versão inicial de uma seção.

    Retorna (section, imported). Por segurança, uma seção já existente
    não é sobrescrita sem force=True. Mesmo com force, o importador
    bloqueia sobrescrita quando a seção já possui mais de uma versão.
    """

    with rx.session() as session:
        section = session.exec(
            select(CmsSection).where(
                CmsSection.page_id == page_id,
                CmsSection.key == key,
            )
        ).first()

        if section is not None:
            if not force:
                return section, False

            versions = list(
                session.exec(
                    select(CmsSectionVersion).where(
                        CmsSectionVersion.section_id
                        == section.id
                    )
                ).all()
            )

            if len(versions) > 1:
                raise RuntimeError(
                    f"A seção '{key}' já possui histórico editorial. "
                    "A importação legada não pode sobrescrevê-la."
                )

            now = _utc_now()
            section.name = name
            section.section_type = section_type
            section.position = position
            section.enabled = True
            section.status = "published"
            section.draft_content = deepcopy(content)
            section.published_content = deepcopy(content)
            section.source_type = "legacy_api"
            section.source_endpoint = source_endpoint
            section.legacy_imported_at = now
            section.published_at = now
            section.updated_at = now

            session.add(section)

            if versions:
                version = versions[0]
                version.content = deepcopy(content)
                version.note = "Conteúdo inicial reimportado da API legada."
                version.published_at = now
                session.add(version)
            else:
                session.add(
                    CmsSectionVersion(
                        section_id=section.id,
                        version_number=1,
                        content=deepcopy(content),
                        note="Conteúdo inicial importado da API legada.",
                        published_at=now,
                    )
                )

            session.commit()
            session.refresh(section)
            return section, True

        now = _utc_now()

        section = CmsSection(
            page_id=page_id,
            key=key,
            name=name,
            section_type=section_type,
            position=position,
            enabled=True,
            status="published",
            draft_content=deepcopy(content),
            published_content=deepcopy(content),
            source_type="legacy_api",
            source_endpoint=source_endpoint,
            legacy_imported_at=now,
            published_at=now,
        )

        session.add(section)
        session.commit()
        session.refresh(section)

        if section.id is None:
            raise RuntimeError(
                "Não foi possível identificar a seção criada."
            )

        version = CmsSectionVersion(
            section_id=section.id,
            version_number=1,
            content=deepcopy(content),
            note="Conteúdo inicial importado da API legada.",
            published_at=now,
        )

        session.add(version)
        session.commit()

        return section, True


def list_page_sections(
    page_key: str,
) -> list[CmsSection]:
    with rx.session() as session:
        page = session.exec(
            select(CmsPage).where(
                CmsPage.key == page_key
            )
        ).first()

        if page is None or page.id is None:
            return []

        return list(
            session.exec(
                select(CmsSection)
                .where(
                    CmsSection.page_id == page.id
                )
                .order_by(
                    CmsSection.position,
                    CmsSection.id,
                )
            ).all()
        )


def list_home_sections() -> list[CmsSection]:
    ensure_home_page()
    return list_page_sections(
        HOME_PAGE_KEY
    )
