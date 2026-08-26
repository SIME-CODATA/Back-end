import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import reflex as rx
from sqlmodel import select

from Back_end.access.modules.auth.model import UserSession


SESSION_DURATION_HOURS = 8


def utc_now() -> datetime:
    """Retorna a data e hora atual em UTC."""

    return datetime.now(timezone.utc)


def hash_session_token(token: str) -> str:
    """Gera o hash SHA-256 usado para armazenar o token da sessão."""

    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_session(user_id: int) -> str:
    """Cria uma nova sessão e retorna o token que será enviado ao navegador."""

    token = secrets.token_urlsafe(48)
    token_hash = hash_session_token(token)

    now = utc_now()

    session_record = UserSession(
        user_id=user_id,
        token_hash=token_hash,
        created_at=now,
        expires_at=now + timedelta(hours=SESSION_DURATION_HOURS),
    )

    with rx.session() as session:
        session.add(session_record)
        session.commit()

    return token


def validate_session(token: str) -> int | None:
    """Valida uma sessão e retorna o ID do usuário autenticado."""

    if not token:
        return None

    token_hash = hash_session_token(token)

    with rx.session() as session:
        session_record = session.exec(
            select(UserSession).where(
                UserSession.token_hash == token_hash
            )
        ).first()

        if session_record is None:
            return None

        if session_record.revoked_at is not None:
            return None

        if session_record.expires_at <= utc_now():
            return None

        return session_record.user_id


def revoke_session(token: str) -> bool:
    """Revoga uma sessão existente."""

    if not token:
        return False

    token_hash = hash_session_token(token)

    with rx.session() as session:
        session_record = session.exec(
            select(UserSession).where(
                UserSession.token_hash == token_hash
            )
        ).first()

        if session_record is None:
            return False

        if session_record.revoked_at is not None:
            return True

        session_record.revoked_at = utc_now()

        session.add(session_record)
        session.commit()

        return True