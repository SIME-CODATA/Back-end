from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import reflex as rx

from Back_end.access.core.guards import can_access
from Back_end.access.core.permissions import Permission
from Back_end.access.states.auth_state import AuthState
from Back_end.smae_scheduler.service import (
    get_schedule,
    list_runs,
    run_sync,
    update_schedule,
)


RunRow = dict[str, str | int]
LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")


def _local_datetime(value: datetime | None) -> str:
    if value is None:
        return "—"
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(LOCAL_TIMEZONE).strftime("%d/%m/%Y %H:%M:%S")


def _source_label(value: str) -> str:
    return {
        "scheduled": "Automático",
        "manual_scheduler": "Manual",
    }.get(str(value or ""), str(value or "—"))


def _status_label(value: str) -> str:
    return {
        "never": "Nunca executado",
        "running": "Em execução",
        "success": "Concluído",
        "failed": "Falhou",
        "busy": "Já havia sincronização",
    }.get(str(value or ""), str(value or "—"))


class SmaeSchedulerState(AuthState):
    loading: bool = False
    saving: bool = False
    running: bool = False

    scheduler_error_message: str = ""
    scheduler_success_message: str = ""

    enabled: bool = False
    mode: str = "daily"
    daily_time: str = "06:00"
    interval_minutes: str = "360"

    last_run: str = "—"
    next_run: str = "—"
    last_status: str = "never"
    last_status_label: str = "Nunca executado"
    last_message: str = ""
    worker_heartbeat: str = "—"

    runs: list[RunRow] = []

    @rx.var
    def can_manage_schedule(self) -> bool:
        return can_access(self.current_user_role, Permission.SCHEDULER_MANAGE)

    def _load_data(self) -> None:
        schedule = get_schedule()

        self.enabled = bool(schedule.enabled)
        self.mode = str(schedule.mode or "daily")
        self.daily_time = str(schedule.daily_time or "06:00")
        self.interval_minutes = str(schedule.interval_minutes or 360)

        self.last_run = _local_datetime(schedule.last_run_at)
        self.next_run = _local_datetime(schedule.next_run_at)
        self.last_status = str(schedule.last_status or "never")
        self.last_status_label = _status_label(self.last_status)
        self.last_message = str(schedule.last_message or "")
        self.worker_heartbeat = _local_datetime(schedule.worker_heartbeat_at)

        self.runs = [
            {
                "id": int(run.id or 0),
                "source": _source_label(run.source),
                "status": str(run.status or ""),
                "status_label": _status_label(run.status),
                "started_at": _local_datetime(run.started_at),
                "finished_at": _local_datetime(run.finished_at),
                "message": str(run.message or ""),
            }
            for run in list_runs(limit=20)
        ]

    @rx.event
    def load_page(self):
        redirect = self._require_permission(Permission.SCHEDULER_VIEW)
        if redirect is not None:
            return redirect

        self.loading = True
        self.scheduler_error_message = ""
        self.scheduler_success_message = ""
        yield

        try:
            self._load_data()
        except Exception as error:
            print(f"Erro ao carregar agendamento SMAE: {error}")
            self.scheduler_error_message = "Não foi possível carregar o agendamento."
        finally:
            self.loading = False

    @rx.event
    def set_enabled(self, value: bool):
        self.enabled = bool(value)

    @rx.event
    def set_mode(self, value: str):
        self.mode = value if value in {"daily", "interval"} else "daily"

    @rx.event
    def set_daily_time(self, value: str):
        self.daily_time = value

    @rx.event
    def set_interval_minutes(self, value: str):
        self.interval_minutes = value

    @rx.event
    def save_schedule(self):
        if not can_access(self.current_user_role, Permission.SCHEDULER_MANAGE):
            self.scheduler_error_message = "Seu perfil não pode alterar o agendamento."
            return

        self.saving = True
        self.scheduler_error_message = ""
        self.scheduler_success_message = ""

        try:
            interval = int(str(self.interval_minutes or "0").strip())
            schedule = update_schedule(
                enabled=self.enabled,
                mode=self.mode,
                daily_time=self.daily_time,
                interval_minutes=interval,
                actor_user_id=self.current_user_id,
            )

            self._audit(
                action="SMAE_SCHEDULE_UPDATED",
                entity_type="smae_schedule",
                entity_id=schedule.id,
                description=(
                    "Agendamento SMAE atualizado: "
                    f"enabled={schedule.enabled}, mode={schedule.mode}, "
                    f"daily_time={schedule.daily_time}, "
                    f"interval_minutes={schedule.interval_minutes}."
                ),
            )

            self._load_data()
            self.scheduler_success_message = "Agendamento salvo com sucesso."
        except Exception as error:
            print(f"Erro ao salvar agendamento SMAE: {error}")
            self.scheduler_error_message = str(error)
        finally:
            self.saving = False

    @rx.event
    async def run_now(self):
        if not can_access(self.current_user_role, Permission.SCHEDULER_MANAGE):
            self.scheduler_error_message = "Seu perfil não pode sincronizar o SMAE."
            return

        self.running = True
        self.scheduler_error_message = ""
        self.scheduler_success_message = ""
        yield

        try:
            run = await asyncio.to_thread(
                run_sync,
                source="manual_scheduler",
                triggered_by=self.current_user_id,
            )
            self._load_data()

            if run.status == "success":
                self._audit(
                    action="SMAE_SYNC",
                    entity_type="smae",
                    description="Sincronização manual executada pela tela de agendamento.",
                )
                self.scheduler_success_message = "Sincronização concluída com sucesso."
            elif run.status == "busy":
                self.scheduler_error_message = run.message
            else:
                self._audit(
                    action="SMAE_SYNC_FAILED",
                    entity_type="smae",
                    description="Falha na sincronização manual pela tela de agendamento.",
                )
                self.scheduler_error_message = run.message or "Falha na sincronização."

        except Exception as error:
            print(f"Erro ao executar sincronização manual do scheduler: {error}")
            self.scheduler_error_message = str(error)
        finally:
            self.running = False
