from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.services.pdm_sync_service import PdmSyncResult, sync_pdm
from Back_end.smae_scheduler.model import SmaeSchedule, SmaeSyncRun
from Back_end.smae_scheduler.sync_lock import (
    SCHEDULER_CLAIM_LOCK_KEY,
    SmaeSyncAlreadyRunningError,
)


DEFAULT_TIMEZONE = "America/Sao_Paulo"
MIN_INTERVAL_MINUTES = 60


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _detach(session, obj):
    session.expunge(obj)
    return obj


def _parse_daily_time(value: str) -> tuple[int, int]:
    raw = str(value or "").strip()
    parts = raw.split(":")

    if len(parts) != 2:
        raise ValueError("Horário deve estar no formato HH:MM.")

    try:
        hour = int(parts[0])
        minute = int(parts[1])
    except ValueError as error:
        raise ValueError("Horário deve estar no formato HH:MM.") from error

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError("Horário inválido.")

    return hour, minute


def calculate_next_run(
    schedule: SmaeSchedule,
    *,
    from_utc: datetime | None = None,
) -> datetime:
    now_utc = from_utc or _utc_now()
    if now_utc.tzinfo is None:
        now_utc = now_utc.replace(tzinfo=timezone.utc)

    if schedule.mode == "interval":
        minutes = max(
            MIN_INTERVAL_MINUTES,
            int(schedule.interval_minutes or MIN_INTERVAL_MINUTES),
        )
        return now_utc + timedelta(minutes=minutes)

    local_tz = ZoneInfo(schedule.timezone_name or DEFAULT_TIMEZONE)
    local_now = now_utc.astimezone(local_tz)
    hour, minute = _parse_daily_time(schedule.daily_time or "06:00")

    candidate = local_now.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )
    if candidate <= local_now:
        candidate += timedelta(days=1)

    return candidate.astimezone(timezone.utc)


def ensure_schedule() -> SmaeSchedule:
    with rx.session() as session:
        schedule = session.exec(
            select(SmaeSchedule).order_by(SmaeSchedule.id)
        ).first()

        if schedule is None:
            schedule = SmaeSchedule(
                enabled=False,
                mode="daily",
                daily_time="06:00",
                interval_minutes=360,
                timezone_name=DEFAULT_TIMEZONE,
            )
            session.add(schedule)
            session.commit()
            session.refresh(schedule)

        return _detach(session, schedule)


def get_schedule() -> SmaeSchedule:
    return ensure_schedule()


def update_schedule(
    *,
    enabled: bool,
    mode: str,
    daily_time: str,
    interval_minutes: int,
    actor_user_id: int | None,
) -> SmaeSchedule:
    normalized_mode = str(mode or "").strip().lower()
    if normalized_mode not in {"daily", "interval"}:
        raise ValueError("Modo de agendamento inválido.")

    normalized_time = str(daily_time or "06:00").strip() or "06:00"
    if normalized_mode == "daily":
        _parse_daily_time(normalized_time)

    try:
        normalized_interval = int(interval_minutes)
    except (TypeError, ValueError) as error:
        raise ValueError("Intervalo inválido.") from error

    if normalized_interval < MIN_INTERVAL_MINUTES:
        raise ValueError(
            f"O menor intervalo permitido é de {MIN_INTERVAL_MINUTES} minutos."
        )

    with rx.session() as session:
        schedule = session.exec(
            select(SmaeSchedule).order_by(SmaeSchedule.id)
        ).first()
        if schedule is None:
            schedule = SmaeSchedule()

        schedule.enabled = bool(enabled)
        schedule.mode = normalized_mode
        schedule.daily_time = normalized_time
        schedule.interval_minutes = normalized_interval
        schedule.timezone_name = DEFAULT_TIMEZONE
        schedule.updated_by = actor_user_id
        schedule.updated_at = _utc_now()
        schedule.next_run_at = (
            calculate_next_run(schedule) if schedule.enabled else None
        )

        session.add(schedule)
        session.commit()
        session.refresh(schedule)
        return _detach(session, schedule)


def list_runs(*, limit: int = 20) -> list[SmaeSyncRun]:
    safe_limit = max(1, min(int(limit), 100))
    with rx.session() as session:
        rows = list(
            session.exec(
                select(SmaeSyncRun)
                .order_by(SmaeSyncRun.started_at.desc(), SmaeSyncRun.id.desc())
                .limit(safe_limit)
            ).all()
        )
        for row in rows:
            session.expunge(row)
        return rows


def _result_dict(result: PdmSyncResult) -> dict:
    return asdict(result)


def run_sync(
    *,
    source: str,
    triggered_by: int | None = None,
) -> SmaeSyncRun:
    started = _utc_now()

    with rx.session() as session:
        run = SmaeSyncRun(
            source=str(source or "scheduled")[:30],
            status="running",
            started_at=started,
            triggered_by=triggered_by,
        )
        session.add(run)
        session.commit()
        session.refresh(run)
        run_id = int(run.id or 0)

    try:
        result = sync_pdm()
        result_data = _result_dict(result)
        status = "success"
        message = (
            f"{result.metas_novas} nova(s) Meta(s), "
            f"{result.metas_atualizadas} Meta(s) atualizada(s), "
            f"{result.detalhes_atualizados} detalhe(s), "
            f"{result.orcamentos_criados + result.orcamentos_atualizados} "
            "orçamento(s) alterado(s) e "
            f"{result.iniciativas_criadas + result.iniciativas_atualizadas} "
            "iniciativa(s) alterada(s)."
        )
    except SmaeSyncAlreadyRunningError as error:
        result_data = {}
        status = "busy"
        message = str(error)
    except Exception as error:
        print(f"Erro na sincronização SMAE do scheduler: {error}")
        result_data = {}
        status = "failed"
        message = str(error)[:1900]

    finished = _utc_now()

    with rx.session() as session:
        run = session.get(SmaeSyncRun, run_id)
        if run is None:
            raise RuntimeError("Execução do scheduler não encontrada.")

        run.status = status
        run.finished_at = finished
        run.message = message
        run.result = result_data
        session.add(run)

        schedule = session.exec(
            select(SmaeSchedule).order_by(SmaeSchedule.id)
        ).first()
        if schedule is not None:
            schedule.last_run_at = finished
            schedule.last_status = status
            schedule.last_message = message
            schedule.updated_at = finished
            schedule.next_run_at = (
                calculate_next_run(schedule, from_utc=finished)
                if schedule.enabled
                else None
            )
            session.add(schedule)

        session.commit()
        session.refresh(run)
        return _detach(session, run)


def run_due_schedule_once() -> SmaeSyncRun | None:
    """
    Uma iteração do worker.

    Uma segunda advisory lock reclama a janela de execução antes do sync.
    Assim vários workers podem existir sem disparar o mesmo horário duas vezes.
    """

    now = _utc_now()

    with rx.session() as session:
        connection = session.connection()
        acquired = bool(
            connection.exec_driver_sql(
                f"SELECT pg_try_advisory_lock({SCHEDULER_CLAIM_LOCK_KEY})"
            ).scalar_one()
        )
        if not acquired:
            return None

        try:
            schedule = session.exec(
                select(SmaeSchedule).order_by(SmaeSchedule.id)
            ).first()
            if schedule is None:
                schedule = SmaeSchedule()
                session.add(schedule)
                session.commit()
                session.refresh(schedule)

            schedule.worker_heartbeat_at = now

            if not schedule.enabled:
                schedule.next_run_at = None
                session.add(schedule)
                session.commit()
                return None

            if schedule.next_run_at is None:
                schedule.next_run_at = calculate_next_run(schedule, from_utc=now)
                session.add(schedule)
                session.commit()
                return None

            next_run = schedule.next_run_at
            if next_run.tzinfo is None:
                next_run = next_run.replace(tzinfo=timezone.utc)

            if next_run > now:
                session.add(schedule)
                session.commit()
                return None

            # Reclama a janela antes de liberar a trava curta.
            schedule.next_run_at = calculate_next_run(schedule, from_utc=now)
            session.add(schedule)
            session.commit()
        finally:
            connection.exec_driver_sql(
                f"SELECT pg_advisory_unlock({SCHEDULER_CLAIM_LOCK_KEY})"
            )

    return run_sync(source="scheduled")
