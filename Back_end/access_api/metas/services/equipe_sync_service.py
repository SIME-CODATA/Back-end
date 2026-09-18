from dataclasses import dataclass

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_equipe import MetaEquipe


@dataclass(frozen=True)
class EquipeSyncResult:
    """Resultado da normalização das equipes das metas."""

    metas_processadas: int
    vinculos_criados: int
    vinculos_removidos: int


def _extract_equipes(
    raw_detail: dict,
    field: str,
) -> list[int]:
    """
    Extrai os IDs das equipes de um bloco do SMAE.

    Exemplo:
    {
        "ps_tecnico_cp": {
            "equipes": [191, 298]
        }
    }
    """

    bloco = raw_detail.get(field) or {}

    equipes = bloco.get("equipes") or []

    return [
        equipe_id
        for equipe_id in equipes
        if isinstance(equipe_id, int)
    ]


def sync_equipes_from_raw_detail() -> EquipeSyncResult:
    """
    Normaliza equipes técnicas e pontos focais
    usando somente metas.raw_detail.

    Não consulta o SMAE.
    """

    metas_processadas = 0
    vinculos_criados = 0
    vinculos_removidos = 0

    with rx.session() as session:
        metas = session.exec(
            select(Meta)
        ).all()

        for meta in metas:
            if meta.id is None:
                continue

            metas_processadas += 1

            raw_detail = meta.raw_detail or {}

            desired_links: set[
                tuple[int, str]
            ] = set()

            # Equipes técnicas
            equipes_tecnicas = _extract_equipes(
                raw_detail,
                "ps_tecnico_cp",
            )

            for equipe_smae_id in equipes_tecnicas:
                desired_links.add(
                    (
                        equipe_smae_id,
                        "tecnico_cp",
                    )
                )

            # Pontos focais
            equipes_ponto_focal = _extract_equipes(
                raw_detail,
                "ps_ponto_focal",
            )

            for equipe_smae_id in equipes_ponto_focal:
                desired_links.add(
                    (
                        equipe_smae_id,
                        "ponto_focal",
                    )
                )

            existing_links = session.exec(
                select(MetaEquipe).where(
                    MetaEquipe.meta_id
                    == meta.id
                )
            ).all()

            existing_keys = {
                (
                    link.equipe_smae_id,
                    link.tipo,
                )
                for link in existing_links
            }

            # Cria os vínculos que ainda não existem.
            for (
                equipe_smae_id,
                tipo,
            ) in desired_links - existing_keys:
                session.add(
                    MetaEquipe(
                        meta_id=meta.id,
                        equipe_smae_id=(
                            equipe_smae_id
                        ),
                        tipo=tipo,
                    )
                )

                vinculos_criados += 1

            # Remove vínculos que desapareceram do SMAE.
            for link in existing_links:
                key = (
                    link.equipe_smae_id,
                    link.tipo,
                )

                if key not in desired_links:
                    session.delete(link)

                    vinculos_removidos += 1

        session.commit()

    return EquipeSyncResult(
        metas_processadas=metas_processadas,
        vinculos_criados=vinculos_criados,
        vinculos_removidos=vinculos_removidos,
    )