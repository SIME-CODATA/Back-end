from dataclasses import dataclass

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.iniciativa import Iniciativa
from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.smae.services.meta_service import (
    fetch_iniciativas_atividades,
)


BATCH_SIZE = 50


@dataclass(frozen=True)
class IniciativaSyncResult:
    """Resultado da sincronização de iniciativas."""

    metas_recebidas: int
    metas_com_iniciativas: int
    iniciativas_criadas: int
    iniciativas_atualizadas: int
    iniciativas_removidas: int
    iniciativas_sem_alteracao: int


def sync_iniciativas() -> IniciativaSyncResult:
    """
    Sincroniza iniciativas das metas com o SMAE.

    Consulta /meta/iniciativas-atividades em lotes.
    """

    with rx.session() as session:
        metas = session.exec(
            select(Meta).order_by(
                Meta.smae_id
            )
        ).all()

        metas_by_smae_id = {
            meta.smae_id: meta
            for meta in metas
        }

        smae_ids = [
            meta.smae_id
            for meta in metas
        ]

    raw_results: list[dict] = []

    for index in range(
        0,
        len(smae_ids),
        BATCH_SIZE,
    ):
        batch = smae_ids[
            index:index + BATCH_SIZE
        ]

        raw_results.extend(
            fetch_iniciativas_atividades(
                batch
            )
        )

    metas_recebidas = 0
    metas_com_iniciativas = 0

    iniciativas_criadas = 0
    iniciativas_atualizadas = 0
    iniciativas_removidas = 0
    iniciativas_sem_alteracao = 0

    with rx.session() as session:
        existing_iniciativas = session.exec(
            select(Iniciativa)
        ).all()

        iniciativas_by_smae_id = {
            iniciativa.smae_id: iniciativa
            for iniciativa in existing_iniciativas
        }

        for raw_meta in raw_results:
            meta_smae_id = raw_meta.get("id")

            if meta_smae_id is None:
                raise RuntimeError(
                    "Resposta de iniciativas sem ID da Meta."
                )

            meta = metas_by_smae_id.get(
                meta_smae_id
            )

            if meta is None:
                raise RuntimeError(
                    f"Meta SMAE {meta_smae_id} "
                    "não encontrada localmente."
                )

            if meta.id is None:
                raise RuntimeError(
                    f"Meta SMAE {meta_smae_id} "
                    "sem ID local."
                )

            metas_recebidas += 1

            raw_iniciativas = (
                raw_meta.get("iniciativas")
                or []
            )

            if raw_iniciativas:
                metas_com_iniciativas += 1

            desired_smae_ids: set[int] = set()

            for raw_iniciativa in raw_iniciativas:
                iniciativa_smae_id = (
                    raw_iniciativa.get("id")
                )

                codigo = raw_iniciativa.get(
                    "codigo"
                )

                titulo = raw_iniciativa.get(
                    "titulo"
                )

                if iniciativa_smae_id is None:
                    raise RuntimeError(
                        f"Iniciativa da Meta "
                        f"{meta_smae_id} sem ID."
                    )

                if not codigo:
                    raise RuntimeError(
                        f"Iniciativa "
                        f"{iniciativa_smae_id} "
                        "sem código."
                    )

                if not titulo:
                    raise RuntimeError(
                        f"Iniciativa "
                        f"{iniciativa_smae_id} "
                        "sem título."
                    )

                desired_smae_ids.add(
                    iniciativa_smae_id
                )

                iniciativa = (
                    iniciativas_by_smae_id.get(
                        iniciativa_smae_id
                    )
                )

                if iniciativa is None:
                    iniciativa = Iniciativa(
                        smae_id=iniciativa_smae_id,
                        meta_id=meta.id,
                        codigo=codigo,
                        titulo=titulo,
                        raw_data=raw_iniciativa,
                    )

                    session.add(iniciativa)
                    session.flush()

                    iniciativas_by_smae_id[
                        iniciativa_smae_id
                    ] = iniciativa

                    iniciativas_criadas += 1

                    continue

                changed = False

                if iniciativa.meta_id != meta.id:
                    iniciativa.meta_id = meta.id
                    changed = True

                if iniciativa.codigo != codigo:
                    iniciativa.codigo = codigo
                    changed = True

                if iniciativa.titulo != titulo:
                    iniciativa.titulo = titulo
                    changed = True

                if (
                    iniciativa.raw_data
                    != raw_iniciativa
                ):
                    iniciativa.raw_data = (
                        raw_iniciativa
                    )
                    changed = True

                if changed:
                    session.add(iniciativa)
                    iniciativas_atualizadas += 1

                else:
                    iniciativas_sem_alteracao += 1

            existing_for_meta = session.exec(
                select(Iniciativa).where(
                    Iniciativa.meta_id
                    == meta.id
                )
            ).all()

            for iniciativa in existing_for_meta:
                if (
                    iniciativa.smae_id
                    not in desired_smae_ids
                ):
                    session.delete(iniciativa)
                    iniciativas_removidas += 1

        session.commit()

    return IniciativaSyncResult(
        metas_recebidas=metas_recebidas,
        metas_com_iniciativas=(
            metas_com_iniciativas
        ),
        iniciativas_criadas=(
            iniciativas_criadas
        ),
        iniciativas_atualizadas=(
            iniciativas_atualizadas
        ),
        iniciativas_removidas=(
            iniciativas_removidas
        ),
        iniciativas_sem_alteracao=(
            iniciativas_sem_alteracao
        ),
    )