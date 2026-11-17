from __future__ import annotations

import asyncio
import os

from Back_end.smae_scheduler.service import run_due_schedule_once


_scheduler_task: asyncio.Task | None = None


async def _scheduler_loop() -> None:
    try:
        poll_seconds = max(
            30,
            int(os.getenv("SMAE_SCHEDULER_POLL_SECONDS", "60")),
        )
    except ValueError:
        poll_seconds = 60

    while True:
        try:
            await asyncio.to_thread(run_due_schedule_once)
        except asyncio.CancelledError:
            raise
        except Exception as error:
            # Migration ausente ou indisponibilidade do banco não derruba a API.
            print(f"[SMAE SCHEDULER] Erro no loop: {error}")

        await asyncio.sleep(poll_seconds)


async def start_scheduler() -> None:
    global _scheduler_task

    if _scheduler_task is not None and not _scheduler_task.done():
        return

    _scheduler_task = asyncio.create_task(_scheduler_loop())
    print("[SMAE SCHEDULER] Agendador iniciado.")


async def stop_scheduler() -> None:
    global _scheduler_task

    if _scheduler_task is None:
        return

    _scheduler_task.cancel()
    try:
        await _scheduler_task
    except asyncio.CancelledError:
        pass

    _scheduler_task = None
    print("[SMAE SCHEDULER] Agendador encerrado.")
