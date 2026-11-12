from __future__ import annotations

from contextlib import contextmanager
from functools import wraps
from typing import Callable, TypeVar

import reflex as rx


SYNC_ADVISORY_LOCK_KEY = 825282026
SCHEDULER_CLAIM_LOCK_KEY = 825282027


class SmaeSyncAlreadyRunningError(RuntimeError):
    """Outra sincronização SMAE já possui a trava global."""


@contextmanager
def smae_sync_lock():
    """
    Serializa qualquer chamada à sincronização completa do SMAE.

    A advisory lock é do PostgreSQL e portanto funciona entre botão manual,
    scheduler e múltiplos processos/containers apontando para o mesmo banco.
    """

    with rx.session() as session:
        connection = session.connection()
        acquired = bool(
            connection.exec_driver_sql(
                f"SELECT pg_try_advisory_lock({SYNC_ADVISORY_LOCK_KEY})"
            ).scalar_one()
        )

        if not acquired:
            raise SmaeSyncAlreadyRunningError(
                "Já existe uma sincronização com o SMAE em andamento."
            )

        try:
            yield
        finally:
            connection.exec_driver_sql(
                f"SELECT pg_advisory_unlock({SYNC_ADVISORY_LOCK_KEY})"
            )


F = TypeVar("F", bound=Callable)


def serialize_smae_sync(function: F) -> F:
    """Decorator aplicado à entrada pública sync_pdm()."""

    @wraps(function)
    def wrapped(*args, **kwargs):
        with smae_sync_lock():
            return function(*args, **kwargs)

    return wrapped  # type: ignore[return-value]
