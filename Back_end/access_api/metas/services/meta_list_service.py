import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta


def list_metas() -> list[dict[str, str]]:
    """Retorna as metas cadastradas para a página de listagem."""

    with rx.session() as session:
        metas = session.exec(
            select(Meta).order_by(Meta.codigo)
        ).all()

        return [
            {
                "codigo": meta.codigo,
                "titulo": meta.titulo,
                "eixo": meta.tema_descricao or "Eixo não informado",
                "url": f"/admin/metas/{meta.codigo}",
            }
            for meta in metas
        ]