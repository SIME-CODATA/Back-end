from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.site_cms.models import (
    CmsMetaContent,
    CmsMetaSyncConflict,
)


_MISSING = object()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _pending_conflict(
    session,
    *,
    meta_content_id: int,
    field_key: str,
) -> CmsMetaSyncConflict | None:
    return session.exec(
        select(CmsMetaSyncConflict).where(
            CmsMetaSyncConflict.meta_content_id
            == meta_content_id,
            CmsMetaSyncConflict.field_key
            == field_key,
            CmsMetaSyncConflict.status
            == "pending",
        )
    ).first()


def _upsert_conflict(
    session,
    *,
    meta_content_id: int,
    field_key: str,
    reason: str,
    previous_smae_value: Any,
    incoming_smae_value: Any,
    cms_value: Any,
) -> CmsMetaSyncConflict:
    conflict = _pending_conflict(
        session,
        meta_content_id=meta_content_id,
        field_key=field_key,
    )

    if conflict is None:
        conflict = CmsMetaSyncConflict(
            meta_content_id=meta_content_id,
            field_key=field_key,
        )

    conflict.reason = reason
    conflict.previous_smae_value = deepcopy(
        previous_smae_value
    )
    conflict.incoming_smae_value = deepcopy(
        incoming_smae_value
    )
    conflict.cms_value = deepcopy(
        cms_value
    )
    conflict.status = "pending"
    conflict.decision = None
    conflict.detected_at = _utc_now()
    conflict.resolved_at = None
    conflict.resolved_by = None

    session.add(conflict)

    return conflict


def apply_smae_snapshot(
    *,
    meta_code: str,
    incoming_snapshot: dict[str, Any],
    smae_meta_id: int | None = None,
) -> dict[str, Any]:
    """
    Aplica uma nova fotografia do SMAE sem destruir personalizações.

    Regras:
    - Campo sem override CMS:
        nova informação do SMAE entra automaticamente no draft.
    - Campo personalizado e SMAE mudou:
        gera conflito para decisão humana.
    - Campo removido do SMAE:
        nunca apaga automaticamente; gera conflito.
    - Campo legado:
        pode ser substituído automaticamente pelo SMAE porque ainda
        não representa personalização do usuário.
    """

    with rx.session() as session:
        meta = session.exec(
            select(CmsMetaContent).where(
                CmsMetaContent.meta_code
                == str(meta_code)
            )
        ).first()

        if meta is None:
            meta = CmsMetaContent(
                meta_code=str(meta_code),
                smae_meta_id=smae_meta_id,
                status="draft",
            )
            session.add(meta)
            session.commit()
            session.refresh(meta)

        if meta.id is None:
            raise RuntimeError(
                "Não foi possível identificar o CMS da Meta."
            )

        old_snapshot = deepcopy(
            meta.smae_snapshot or {}
        )
        draft = deepcopy(
            meta.draft_content or {}
        )
        source_map = deepcopy(
            meta.source_map or {}
        )

        changed_fields: list[str] = []
        conflict_fields: list[str] = []
        added_fields: list[str] = []

        all_keys = set(
            old_snapshot.keys()
        ) | set(
            incoming_snapshot.keys()
        )

        for field_key in sorted(
            all_keys
        ):
            old_value = old_snapshot.get(
                field_key,
                _MISSING,
            )
            new_value = incoming_snapshot.get(
                field_key,
                _MISSING,
            )

            if (
                old_value is not _MISSING
                and new_value is not _MISSING
                and old_value == new_value
            ):
                continue

            current_source = source_map.get(
                field_key,
                "legacy",
            )

            current_cms_value = draft.get(
                field_key
            )

            # SMAE deixou de trazer o campo:
            # nunca apagamos automaticamente.
            if new_value is _MISSING:
                _upsert_conflict(
                    session,
                    meta_content_id=meta.id,
                    field_key=field_key,
                    reason="removed_from_smae",
                    previous_smae_value=(
                        None
                        if old_value is _MISSING
                        else old_value
                    ),
                    incoming_smae_value=None,
                    cms_value=current_cms_value,
                )
                conflict_fields.append(
                    field_key
                )
                continue

            # Houve personalização explícita no CMS:
            # a decisão passa para o usuário.
            if current_source == "cms":
                _upsert_conflict(
                    session,
                    meta_content_id=meta.id,
                    field_key=field_key,
                    reason="changed_in_smae",
                    previous_smae_value=(
                        None
                        if old_value is _MISSING
                        else old_value
                    ),
                    incoming_smae_value=new_value,
                    cms_value=current_cms_value,
                )
                conflict_fields.append(
                    field_key
                )
                continue

            # Sem personalização: atualiza o draft automaticamente.
            was_new = (
                old_value is _MISSING
            )

            draft[field_key] = deepcopy(
                new_value
            )
            source_map[field_key] = "smae"

            changed_fields.append(
                field_key
            )

            if was_new:
                added_fields.append(
                    field_key
                )

        meta.smae_snapshot = deepcopy(
            incoming_snapshot
        )
        meta.draft_content = draft
        meta.source_map = source_map
        meta.smae_meta_id = (
            smae_meta_id
            if smae_meta_id is not None
            else meta.smae_meta_id
        )
        meta.smae_synced_at = _utc_now()
        meta.updated_at = _utc_now()
        meta.status = (
            "published"
            if draft
            == meta.published_content
            else "draft"
        )

        session.add(meta)
        session.commit()

        return {
            "meta_code": str(meta_code),
            "changed_fields": changed_fields,
            "added_fields": added_fields,
            "conflict_fields": conflict_fields,
        }


def list_pending_conflicts(
    *,
    meta_code: str,
) -> list[CmsMetaSyncConflict]:
    with rx.session() as session:
        meta = session.exec(
            select(CmsMetaContent).where(
                CmsMetaContent.meta_code
                == str(meta_code)
            )
        ).first()

        if meta is None or meta.id is None:
            return []

        return list(
            session.exec(
                select(CmsMetaSyncConflict)
                .where(
                    CmsMetaSyncConflict.meta_content_id
                    == meta.id,
                    CmsMetaSyncConflict.status
                    == "pending",
                )
                .order_by(
                    CmsMetaSyncConflict.detected_at,
                    CmsMetaSyncConflict.id,
                )
            ).all()
        )


def resolve_conflict(
    *,
    conflict_id: int,
    decision: str,
    actor_user_id: int | None,
) -> CmsMetaSyncConflict:
    """
    Resolve um conflito individual.

    decision:
    - keep_cms
    - use_smae
    """

    if decision not in {
        "keep_cms",
        "use_smae",
    }:
        raise ValueError(
            "Decisão de conflito inválida."
        )

    with rx.session() as session:
        conflict = session.get(
            CmsMetaSyncConflict,
            conflict_id,
        )

        if (
            conflict is None
            or conflict.status != "pending"
        ):
            raise ValueError(
                "Conflito não encontrado ou já resolvido."
            )

        meta = session.get(
            CmsMetaContent,
            conflict.meta_content_id,
        )

        if meta is None:
            raise ValueError(
                "Conteúdo editorial da Meta não encontrado."
            )

        draft = deepcopy(
            meta.draft_content or {}
        )
        source_map = deepcopy(
            meta.source_map or {}
        )

        if decision == "use_smae":
            # Em remoção, a escolha "usar SMAE" remove o campo do draft.
            if (
                conflict.reason
                == "removed_from_smae"
            ):
                draft.pop(
                    conflict.field_key,
                    None,
                )
                source_map.pop(
                    conflict.field_key,
                    None,
                )
            else:
                draft[
                    conflict.field_key
                ] = deepcopy(
                    conflict.incoming_smae_value
                )
                source_map[
                    conflict.field_key
                ] = "smae"

        else:
            # Manter CMS cria/ratifica um override editorial.
            source_map[
                conflict.field_key
            ] = "cms"

        meta.draft_content = draft
        meta.source_map = source_map
        meta.status = (
            "published"
            if draft
            == meta.published_content
            else "draft"
        )
        meta.updated_by = actor_user_id
        meta.updated_at = _utc_now()

        conflict.status = "resolved"
        conflict.decision = decision
        conflict.resolved_by = actor_user_id
        conflict.resolved_at = _utc_now()

        session.add(meta)
        session.add(conflict)
        session.commit()
        session.refresh(conflict)

        return conflict


def resolve_all_conflicts(
    *,
    meta_code: str,
    decision: str,
    actor_user_id: int | None,
) -> int:
    conflicts = list_pending_conflicts(
        meta_code=meta_code
    )

    for conflict in conflicts:
        if conflict.id is None:
            continue

        resolve_conflict(
            conflict_id=conflict.id,
            decision=decision,
            actor_user_id=actor_user_id,
        )

    return len(conflicts)
