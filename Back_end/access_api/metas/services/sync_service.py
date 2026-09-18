from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta, utc_now
from Back_end.access_api.metas.models.meta_orcamento import MetaOrcamento
from Back_end.access_api.smae.services.meta_service import ( fetch_meta_detail, fetch_meta_details, fetch_metas,)


@dataclass(frozen=True)
class MetaSyncResult:
    """Resultado de uma sincronização de metas com o SMAE."""

    received: int
    inserted: int
    updated: int
    unchanged: int

@dataclass(frozen=True)
class MetaDetailsBatchSyncResult:
    """Resultado da sincronização detalhada em lote."""

    received: int
    metas_updated: int
    budgets_created: int
    budgets_updated: int
    budgets_unchanged: int

@dataclass(frozen=True)
class MetaDetailSyncResult:
    """Resultado da sincronização detalhada de uma única meta."""

    smae_id: int

    meta_created: bool
    meta_updated: bool

    budget_available: bool
    budget_created: bool
    budget_updated: bool


def _normalize_meta(raw_meta: dict) -> dict:
    """
    Transforma uma Meta recebida da listagem do SMAE
    no formato básico usado localmente.

    Essa função continua sendo usada pelo sync geral das 132 metas.
    """

    smae_id = raw_meta.get("id")
    pdm_id = raw_meta.get("pdm_id")
    codigo = raw_meta.get("codigo")
    titulo = raw_meta.get("titulo")

    if smae_id is None:
        raise RuntimeError(
            "Meta recebida do SMAE sem id."
        )

    if pdm_id is None:
        raise RuntimeError(
            f"Meta SMAE {smae_id} recebida sem pdm_id."
        )

    if not codigo:
        raise RuntimeError(
            f"Meta SMAE {smae_id} recebida sem código."
        )

    if not titulo:
        raise RuntimeError(
            f"Meta SMAE {smae_id} recebida sem título."
        )

    tema = raw_meta.get("tema") or {}

    return {
        "smae_id": smae_id,
        "pdm_id": pdm_id,
        "codigo": codigo,
        "titulo": titulo,
        "contexto": raw_meta.get("contexto"),
        "complemento": raw_meta.get("complemento"),
        "ativo": bool(
            raw_meta.get("ativo", False)
        ),
        "tema_smae_id": tema.get("id"),
        "tema_descricao": tema.get("descricao"),
    }


def _normalize_meta_detail(
    raw_meta: dict,
) -> dict:
    """
    Normaliza os dados completos retornados por /meta/{id}.

    Além dos dados básicos, armazena macrotema, subtema,
    cronograma e o payload completo sanitizado.
    """

    meta_data = _normalize_meta(raw_meta)

    macro_tema = (
        raw_meta.get("macro_tema") or {}
    )

    sub_tema = (
        raw_meta.get("sub_tema") or {}
    )

    cronograma = (
        raw_meta.get("cronograma") or {}
    )

    meta_data.update(
        {
            "status": raw_meta.get("status"),

            "macro_tema_smae_id": (
                macro_tema.get("id")
            ),
            "macro_tema_descricao": (
                macro_tema.get("descricao")
            ),

            "sub_tema_smae_id": (
                sub_tema.get("id")
            ),
            "sub_tema_descricao": (
                sub_tema.get("descricao")
            ),

            "cronograma_smae_id": (
                cronograma.get("id")
            ),
            "atraso_grau": (
                cronograma.get("atraso_grau")
            ),

            # O retorno já chega sanitizado pelo meta_service.
            "raw_detail": raw_meta,
        }
    )

    return meta_data


def _to_decimal(
    value: object,
) -> Decimal | None:
    """
    Converte valores monetários recebidos do SMAE
    para Decimal.
    """

    if value is None or value == "":
        return None

    try:
        return Decimal(str(value))

    except (
        InvalidOperation,
        ValueError,
        TypeError,
    ) as error:
        raise RuntimeError(
            f"Valor monetário inválido recebido do SMAE: {value}"
        ) from error


def _parse_datetime(
    value: object,
) -> datetime | None:
    """
    Converte datas ISO 8601 retornadas pelo SMAE
    para datetime com timezone.
    """

    if value is None or value == "":
        return None

    if isinstance(value, datetime):
        return value

    try:
        normalized_value = str(value).replace(
            "Z",
            "+00:00",
        )

        return datetime.fromisoformat(
            normalized_value
        )

    except ValueError as error:
        raise RuntimeError(
            f"Data inválida recebida do SMAE: {value}"
        ) from error


def _normalize_budget(
    raw_budget: dict | None,
) -> dict | None:
    """Normaliza o orçamento retornado pelo SMAE."""

    if not raw_budget:
        return None

    money_fields = (
        "total_previsao",
        "total_empenhado",
        "total_liquidado",

        "total_previsao_projeto",
        "total_empenhado_projeto",
        "total_liquidado_projeto",

        "total_previsao_atividade",
        "total_empenhado_atividade",
        "total_liquidado_atividade",

        "total_previsao_operacao_especial",
        "total_empenhado_operacao_especial",
        "total_liquidado_operacao_especial",
    )

    budget_data = {
        field: _to_decimal(
            raw_budget.get(field)
        )
        for field in money_fields
    }

    budget_data["atualizado_em"] = (
        _parse_datetime(
            raw_budget.get("atualizado_em")
        )
    )

    return budget_data


def sync_metas() -> MetaSyncResult:
    """
    Sincroniza a listagem geral das metas do SMAE
    com o PostgreSQL local.

    Dados detalhados já existentes não são apagados.
    """

    raw_metas = fetch_metas()

    normalized_metas = [
        _normalize_meta(raw_meta)
        for raw_meta in raw_metas
    ]

    incoming_ids = [
        meta["smae_id"]
        for meta in normalized_metas
    ]

    inserted = 0
    updated = 0
    unchanged = 0

    now = utc_now()

    with rx.session() as session:
        existing_metas = []

        if incoming_ids:
            existing_metas = session.exec(
                select(Meta).where(
                    Meta.smae_id.in_(
                        incoming_ids
                    )
                )
            ).all()

        existing_by_smae_id = {
            meta.smae_id: meta
            for meta in existing_metas
        }

        for meta_data in normalized_metas:
            smae_id = meta_data["smae_id"]

            existing_meta = (
                existing_by_smae_id.get(
                    smae_id
                )
            )

            if existing_meta is None:
                meta = Meta(
                    **meta_data,
                    created_at=now,
                    updated_at=now,
                    synced_at=now,
                )

                session.add(meta)

                inserted += 1
                continue

            changed = False

            for field, value in (
                meta_data.items()
            ):
                if field == "smae_id":
                    continue

                current_value = getattr(
                    existing_meta,
                    field,
                )

                if current_value != value:
                    setattr(
                        existing_meta,
                        field,
                        value,
                    )

                    changed = True

            if changed:
                existing_meta.updated_at = now
                updated += 1

            else:
                unchanged += 1

            existing_meta.synced_at = now

            session.add(
                existing_meta
            )

        session.commit()

    return MetaSyncResult(
        received=len(normalized_metas),
        inserted=inserted,
        updated=updated,
        unchanged=unchanged,
    )

def _apply_meta_detail( session, raw_meta: dict,) -> tuple[bool, bool, bool, bool]:
    """
    Persiste o detalhe completo de uma meta já obtido do SMAE.

    Retorna:
        meta_updated,
        budget_created,
        budget_updated,
        budget_unchanged
    """

    smae_id = raw_meta.get("id")

    if smae_id is None:
        raise RuntimeError(
            "Detalhe de meta recebido sem id."
        )

    meta_data = _normalize_meta_detail(
        raw_meta
    )

    budget_data = _normalize_budget(
        raw_meta.get("orcamento")
    )

    now = utc_now()

    meta = session.exec(
        select(Meta).where(
            Meta.smae_id == smae_id
        )
    ).first()

    if meta is None:
        meta = Meta(
            **meta_data,
            created_at=now,
            updated_at=now,
            synced_at=now,
        )

        session.add(meta)
        session.flush()

        meta_updated = True

    else:
        changed = False

        for field, value in meta_data.items():
            if field == "smae_id":
                continue

            if getattr(meta, field) != value:
                setattr(
                    meta,
                    field,
                    value,
                )
                changed = True

        if changed:
            meta.updated_at = now

        meta.synced_at = now

        session.add(meta)
        session.flush()

        meta_updated = changed

    if meta.id is None:
        raise RuntimeError(
            f"Meta SMAE {smae_id} "
            "não possui ID local."
        )

    budget_created = False
    budget_updated = False
    budget_unchanged = False

    if budget_data is not None:
        budget = session.exec(
            select(
                MetaOrcamento
            ).where(
                MetaOrcamento.meta_id
                == meta.id
            )
        ).first()

        if budget is None:
            budget = MetaOrcamento(
                meta_id=meta.id,
                **budget_data,
            )

            session.add(budget)

            budget_created = True

        else:
            changed = False

            for field, value in (
                budget_data.items()
            ):
                if getattr(
                    budget,
                    field,
                ) != value:
                    setattr(
                        budget,
                        field,
                        value,
                    )
                    changed = True

            if changed:
                session.add(budget)
                budget_updated = True
            else:
                budget_unchanged = True

    return (
        meta_updated,
        budget_created,
        budget_updated,
        budget_unchanged,
    )

def sync_all_meta_details() -> MetaDetailsBatchSyncResult:
    """
    Sincroniza os detalhes completos de todas
    as metas já cadastradas localmente.
    """

    with rx.session() as session:
        metas = session.exec(
            select(Meta).order_by(
                Meta.smae_id
            )
        ).all()

        smae_ids = [
            meta.smae_id
            for meta in metas
        ]

    raw_details = fetch_meta_details(
        smae_ids
    )

    metas_updated = 0
    budgets_created = 0
    budgets_updated = 0
    budgets_unchanged = 0

    with rx.session() as session:
        for raw_meta in raw_details:
            (
                meta_updated,
                budget_created,
                budget_updated,
                budget_unchanged,
            ) = _apply_meta_detail(
                session,
                raw_meta,
            )

            if meta_updated:
                metas_updated += 1

            if budget_created:
                budgets_created += 1

            if budget_updated:
                budgets_updated += 1

            if budget_unchanged:
                budgets_unchanged += 1

        session.commit()

    return MetaDetailsBatchSyncResult(
        received=len(raw_details),
        metas_updated=metas_updated,
        budgets_created=budgets_created,
        budgets_updated=budgets_updated,
        budgets_unchanged=budgets_unchanged,
    )

def sync_meta_detail(
    smae_id: int,
) -> MetaDetailSyncResult:
    """
    Sincroniza todos os dados disponíveis de uma única Meta.

    Busca /meta/{id} e atualiza:
    - dados principais da meta;
    - macrotema;
    - tema;
    - subtema;
    - cronograma;
    - payload completo;
    - orçamento.
    """

    raw_meta = fetch_meta_detail(
        smae_id
    )

    meta_data = _normalize_meta_detail(
        raw_meta
    )

    budget_data = _normalize_budget(
        raw_meta.get("orcamento")
    )

    now = utc_now()

    meta_created = False
    meta_updated = False

    budget_created = False
    budget_updated = False

    with rx.session() as session:
        existing_meta = session.exec(
            select(Meta).where(
                Meta.smae_id == smae_id
            )
        ).first()

        if existing_meta is None:
            meta = Meta(
                **meta_data,
                created_at=now,
                updated_at=now,
                synced_at=now,
            )

            session.add(meta)
            session.flush()

            meta_created = True

        else:
            meta = existing_meta

            changed = False

            for field, value in (
                meta_data.items()
            ):
                if field == "smae_id":
                    continue

                current_value = getattr(
                    meta,
                    field,
                )

                if current_value != value:
                    setattr(
                        meta,
                        field,
                        value,
                    )

                    changed = True

            if changed:
                meta.updated_at = now
                meta_updated = True

            meta.synced_at = now

            session.add(meta)
            session.flush()

        if meta.id is None:
            raise RuntimeError(
                f"Meta SMAE {smae_id} "
                "não possui ID local após persistência."
            )

        if budget_data is not None:
            existing_budget = session.exec(
                select(
                    MetaOrcamento
                ).where(
                    MetaOrcamento.meta_id
                    == meta.id
                )
            ).first()

            if existing_budget is None:
                budget = MetaOrcamento(
                    meta_id=meta.id,
                    **budget_data,
                )

                session.add(budget)

                budget_created = True

            else:
                changed = False

                for field, value in (
                    budget_data.items()
                ):
                    current_value = getattr(
                        existing_budget,
                        field,
                    )

                    if current_value != value:
                        setattr(
                            existing_budget,
                            field,
                            value,
                        )

                        changed = True

                if changed:
                    session.add(
                        existing_budget
                    )

                    budget_updated = True

        session.commit()

    return MetaDetailSyncResult(
        smae_id=smae_id,

        meta_created=meta_created,
        meta_updated=meta_updated,

        budget_available=(
            budget_data is not None
        ),

        budget_created=budget_created,
        budget_updated=budget_updated,
    )