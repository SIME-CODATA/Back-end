from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel

from Back_end.access.modules.users.model import User  # noqa: F401


def utc_now() -> datetime:
    """Retorna a data e hora atual em UTC."""

    return datetime.now(timezone.utc)


class UserSession(SQLModel, table=True):
    """Sessão autenticada de um usuário do painel administrativo."""

    __tablename__ = "user_sessions"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    user_id: int = Field(
        foreign_key="users.id",
        index=True,
    )

    token_hash: str = Field(
        index=True,
        unique=True,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    expires_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    revoked_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )