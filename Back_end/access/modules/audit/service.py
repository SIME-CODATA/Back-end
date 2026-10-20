import reflex as rx
from sqlmodel import select

from Back_end.access.modules.audit.model import AuditLog


def create_audit_log(
    *,
    action: str,
    entity_type: str = "system",
    entity_id: str | int | None = None,
    description: str = "",
    actor_user_id: int | None = None,
    actor_name: str = "",
    actor_email: str = "",
    actor_role: str = "",
    ip_address: str | None = None,
) -> int | None:
    """
    Registra uma ação administrativa no histórico.
    """

    audit = AuditLog(
        actor_user_id=actor_user_id,
        actor_name=actor_name,
        actor_email=actor_email,
        actor_role=actor_role,
        action=action,
        entity_type=entity_type,
        entity_id=(
            str(entity_id)
            if entity_id is not None
            else None
        ),
        description=description,
        ip_address=ip_address,
    )

    with rx.session() as session:
        session.add(audit)
        session.commit()
        session.refresh(audit)

        return audit.id


def get_recent_audit_logs(
    limit: int = 100,
) -> list[AuditLog]:
    """
    Retorna os registros mais recentes.
    """

    with rx.session() as session:
        statement = (
            select(AuditLog)
            .order_by(
                AuditLog.created_at.desc()
            )
            .limit(limit)
        )

        return list(
            session.exec(statement).all()
        )