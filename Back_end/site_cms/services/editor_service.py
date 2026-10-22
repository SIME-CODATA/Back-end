import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import (
    CmsPage,
    CmsSection,
    CmsSectionVersion,
)


def get_cms_section(
    *,
    page_key: str,
    section_key: str,
) -> CmsSection | None:
    """Busca uma seção dentro da página correta do CMS."""

    with rx.session() as session:
        page = session.exec(
            select(CmsPage).where(
                CmsPage.key == page_key
            )
        ).first()

        if page is None or page.id is None:
            return None

        return session.exec(
            select(CmsSection).where(
                CmsSection.page_id == page.id,
                CmsSection.key == section_key,
            )
        ).first()


def list_section_versions(
    section_id: int,
) -> list[CmsSectionVersion]:
    return list(
        _list_versions(section_id)
    )


def _list_versions(
    section_id: int,
):
    with rx.session() as session:
        return session.exec(
            select(CmsSectionVersion)
            .where(
                CmsSectionVersion.section_id == section_id
            )
            .order_by(
                CmsSectionVersion.version_number.desc(),
                CmsSectionVersion.id.desc(),
            )
        ).all()
