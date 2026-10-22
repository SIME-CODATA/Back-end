from collections import defaultdict
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.iniciativa import Iniciativa
from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orgao import MetaOrgao
from Back_end.access_api.metas.models.meta_tag import MetaTag
from Back_end.access_api.metas.models.orgao import Orgao
from Back_end.access_api.metas.models.tag import Tag

from Back_end.site_cms.modules.metas.code import (
    canonical_meta_code,
)
from Back_end.site_cms.modules.metas.sync_service import (
    apply_smae_snapshot,
)


ANDAMENTO_TO_SITE = {
    "Em planejamento": "planejamento",
    "Em progresso": "progresso",
    "Atingida": "atingida",
}


def _find_monitoring(
    descriptions: set[str],
) -> str | None:
    for label, normalized in (
        ANDAMENTO_TO_SITE.items()
    ):
        if label in descriptions:
            return normalized

    return None


def _build_local_snapshots() -> list[dict[str, Any]]:
    """
    Monta snapshots somente com dados já sincronizados no PostgreSQL.

    Não faz nova requisição HTTP ao SMAE.
    """

    with rx.session() as session:
        metas = list(
            session.exec(
                select(Meta).order_by(
                    Meta.codigo
                )
            ).all()
        )

        orgao_rows = session.exec(
            select(
                MetaOrgao.meta_id,
                Orgao.sigla,
                Orgao.descricao,
                MetaOrgao.responsavel,
            )
            .join(
                Orgao,
                Orgao.id
                == MetaOrgao.orgao_id,
            )
        ).all()

        tag_rows = session.exec(
            select(
                MetaTag.meta_id,
                Tag.descricao,
            )
            .join(
                Tag,
                Tag.id
                == MetaTag.tag_id,
            )
        ).all()

        iniciativas = list(
            session.exec(
                select(Iniciativa).order_by(
                    Iniciativa.meta_id,
                    Iniciativa.codigo,
                )
            ).all()
        )

    orgaos_by_meta: dict[
        int,
        list[str],
    ] = defaultdict(list)

    for (
        meta_id,
        sigla,
        descricao,
        responsavel,
    ) in orgao_rows:
        if not responsavel:
            continue

        value = str(
            sigla
            or descricao
            or ""
        ).strip()

        if value:
            orgaos_by_meta[
                int(meta_id)
            ].append(value)

    tags_by_meta: dict[
        int,
        set[str],
    ] = defaultdict(set)

    for meta_id, descricao in tag_rows:
        if descricao:
            tags_by_meta[
                int(meta_id)
            ].add(
                str(descricao)
            )

    iniciativas_by_meta: dict[
        int,
        list[dict[str, str]],
    ] = defaultdict(list)

    for iniciativa in iniciativas:
        iniciativas_by_meta[
            int(iniciativa.meta_id)
        ].append({
            "number": str(
                iniciativa.codigo
                or ""
            ),
            "description": str(
                iniciativa.titulo
                or ""
            ),
        })

    result: list[
        dict[str, Any]
    ] = []

    for meta in metas:
        if meta.id is None:
            continue

        code = canonical_meta_code(
            meta.codigo
        )

        snapshot: dict[
            str,
            Any,
        ] = {
            "number": code,
            "title": str(
                meta.titulo
                or ""
            ),
            "projection": str(
                meta.contexto
                or ""
            ),
            "responsible_agencies": (
                sorted(
                    set(
                        orgaos_by_meta.get(
                            int(meta.id),
                            [],
                        )
                    ),
                    key=str.casefold,
                )
            ),
            "axis_name": str(
                meta.tema_descricao
                or ""
            ),
        }

        monitoring = _find_monitoring(
            tags_by_meta.get(
                int(meta.id),
                set(),
            )
        )

        if monitoring:
            snapshot[
                "monitoring"
            ] = monitoring

        # ----------------------------------------------------
        # AÇÕES ESTRATÉGICAS
        # ----------------------------------------------------
        #
        # O banco local do SMAE hoje possui código/título das iniciativas,
        # mas o site antigo possui também:
        # - concluída
        # - evolução em destaque
        # - descrição da evolução
        #
        # Portanto não substituímos strategic_actions ainda.
        # Guardamos a lista encontrada apenas como informação auxiliar
        # no resultado desta função para futura evolução do mapeamento.
        # ----------------------------------------------------

        result.append({
            "meta_code": code,
            "smae_meta_id": (
                meta.smae_id
            ),
            "snapshot": snapshot,
            "available_initiatives": (
                iniciativas_by_meta.get(
                    int(meta.id),
                    [],
                )
            ),
        })

    return result


def sync_cms_meta_snapshots_from_local() -> dict[str, Any]:
    """
    Atualiza a camada editorial com a última fotografia do SMAE local.

    Personalizações CMS nunca são sobrescritas automaticamente.
    """

    snapshots = (
        _build_local_snapshots()
    )

    processed = 0
    changed = 0
    conflicts = 0
    added = 0

    per_meta: list[
        dict[str, Any]
    ] = []

    for item in snapshots:
        result = apply_smae_snapshot(
            meta_code=item[
                "meta_code"
            ],
            incoming_snapshot=item[
                "snapshot"
            ],
            smae_meta_id=item[
                "smae_meta_id"
            ],
        )

        processed += 1

        changed += len(
            result[
                "changed_fields"
            ]
        )
        added += len(
            result[
                "added_fields"
            ]
        )
        conflicts += len(
            result[
                "conflict_fields"
            ]
        )

        per_meta.append(
            result
        )

    return {
        "processed": processed,
        "changed_fields": changed,
        "added_fields": added,
        "conflicts": conflicts,
        "metas": per_meta,
    }
