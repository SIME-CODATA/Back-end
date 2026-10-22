from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # Snapshot do usuário no momento da ação.
    # Não usamos FK aqui para preservar o histórico
    # mesmo se o usuário for excluído depois.
    actor_user_id: int | None = Field(
        default=None,
        index=True,
    )

    actor_name: str = Field(
        default="",
        max_length=150,
    )

    actor_email: str = Field(
        default="",
        max_length=255,
        index=True,
    )

    actor_role: str = Field(
        default="",
        max_length=20,
    )

    # Ex.: LOGIN, USER_CREATED, SMAE_SYNC
    action: str = Field(
        index=True,
        max_length=50,
    )

    # Ex.: user, smae, authentication
    entity_type: str = Field(
        default="system",
        index=True,
        max_length=50,
    )

    # ID do registro afetado, quando existir.
    entity_id: str | None = Field(
        default=None,
        max_length=100,
    )

    description: str = Field(
        default="",
        max_length=500,
    )

    ip_address: str | None = Field(
        default=None,
        max_length=45,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ),
        index=True,
    )