from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _tz_datetime(*, nullable: bool, index: bool = False):
    return Column(DateTime(timezone=True), nullable=nullable, index=index)


class SmaeSchedule(SQLModel, table=True):
    """Configuração única do agendamento automático do SMAE."""

    __tablename__ = "smae_schedules"

    id: int | None = Field(default=None, primary_key=True)

    enabled: bool = Field(default=False, index=True)
    mode: str = Field(default="daily", max_length=20)
    daily_time: str = Field(default="06:00", max_length=5)
    interval_minutes: int = Field(default=360)
    timezone_name: str = Field(default="America/Sao_Paulo", max_length=80)

    last_run_at: datetime | None = Field(
        default=None,
        sa_column=_tz_datetime(nullable=True, index=True),
    )
    next_run_at: datetime | None = Field(
        default=None,
        sa_column=_tz_datetime(nullable=True, index=True),
    )

    last_status: str = Field(default="never", max_length=30, index=True)
    last_message: str = Field(default="", max_length=1500)

    worker_heartbeat_at: datetime | None = Field(
        default=None,
        sa_column=_tz_datetime(nullable=True, index=True),
    )

    updated_by: int | None = Field(default=None, index=True)

    created_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=_tz_datetime(nullable=False, index=True),
    )
    updated_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=_tz_datetime(nullable=False, index=True),
    )


class SmaeSyncRun(SQLModel, table=True):
    """Histórico das tentativas disparadas pelo agendador."""

    __tablename__ = "smae_sync_runs"

    id: int | None = Field(default=None, primary_key=True)
    source: str = Field(default="scheduled", max_length=30, index=True)
    status: str = Field(default="running", max_length=30, index=True)

    started_at: datetime = Field(
        default_factory=_utc_now,
        sa_column=_tz_datetime(nullable=False, index=True),
    )
    finished_at: datetime | None = Field(
        default=None,
        sa_column=_tz_datetime(nullable=True, index=True),
    )

    message: str = Field(default="", max_length=2000)
    result: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSONB, nullable=False),
    )

    triggered_by: int | None = Field(default=None, index=True)
