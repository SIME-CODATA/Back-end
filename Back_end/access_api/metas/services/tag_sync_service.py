from dataclasses import dataclass

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_tag import MetaTag
from Back_end.access_api.metas.models.tag import Tag


@dataclass(frozen=True)
class TagSyncResult:
    """Resultado da normalização das tags das metas."""

    metas_processadas: int
    tags_criadas: int
    tags_atualizadas: int
    vinculos_criados: int
    vinculos_removidos: int


def sync_tags_from_raw_detail() -> TagSyncResult:
    """
    Normaliza as tags existentes em metas.raw_detail.

    Não consulta o SMAE.
    Trabalha apenas com os dados completos já persistidos localmente.
    """

    metas_processadas = 0
    tags_criadas = 0
    tags_atualizadas = 0
    vinculos_criados = 0
    vinculos_removidos = 0

    with rx.session() as session:
        metas = session.exec(
            select(Meta)
        ).all()

        existing_tags = session.exec(
            select(Tag)
        ).all()

        tags_by_smae_id = {
            tag.smae_id: tag
            for tag in existing_tags
        }

        for meta in metas:
            raw_detail = meta.raw_detail or {}

            raw_tags = raw_detail.get("tags") or []

            metas_processadas += 1

            desired_tag_ids: set[int] = set()

            for raw_tag in raw_tags:
                smae_id = raw_tag.get("id")
                descricao = raw_tag.get("descricao")

                if smae_id is None or not descricao:
                    continue

                tag = tags_by_smae_id.get(smae_id)

                if tag is None:
                    tag = Tag(
                        smae_id=smae_id,
                        descricao=descricao,
                    )

                    session.add(tag)
                    session.flush()

                    tags_by_smae_id[smae_id] = tag

                    tags_criadas += 1

                elif tag.descricao != descricao:
                    tag.descricao = descricao

                    session.add(tag)

                    tags_atualizadas += 1

                if tag.id is None:
                    raise RuntimeError(
                        f"Tag SMAE {smae_id} sem ID local."
                    )

                desired_tag_ids.add(tag.id)

            existing_links = session.exec(
                select(MetaTag).where(
                    MetaTag.meta_id == meta.id
                )
            ).all()

            existing_tag_ids = {
                link.tag_id
                for link in existing_links
            }

            # Cria vínculos que ainda não existem.
            for tag_id in (
                desired_tag_ids - existing_tag_ids
            ):
                session.add(
                    MetaTag(
                        meta_id=meta.id,
                        tag_id=tag_id,
                    )
                )

                vinculos_criados += 1

            # Remove vínculos que deixaram de existir no SMAE.
            for link in existing_links:
                if link.tag_id not in desired_tag_ids:
                    session.delete(link)

                    vinculos_removidos += 1

        session.commit()

    return TagSyncResult(
        metas_processadas=metas_processadas,
        tags_criadas=tags_criadas,
        tags_atualizadas=tags_atualizadas,
        vinculos_criados=vinculos_criados,
        vinculos_removidos=vinculos_removidos,
    )