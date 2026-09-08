import reflex as rx
from sqlmodel import select

from Back_end.metas.models.meta import Meta


def list_metas() -> list[Meta]:
    """Lista as metas persistidas localmente, ordenadas pelo código."""

    with rx.session() as session:
        metas = session.exec(
            select(Meta).order_by(Meta.codigo)
        ).all()

        return list(metas)