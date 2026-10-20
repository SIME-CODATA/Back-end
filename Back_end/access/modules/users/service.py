from datetime import datetime, timezone

import reflex as rx
from sqlmodel import select

from Back_end.access.core.email_policy import (
    validate_allowed_email,
)
from Back_end.access.core.roles import (
    UserRole,
    normalize_role,
)
from Back_end.access.core.security import (
    hash_password,
    verify_password,
)
from Back_end.access.modules.auth.model import UserSession
from Back_end.access.modules.auth.service import (
    hash_session_token,
)
from Back_end.access.modules.users.model import User


MANAGER_ROLES = {
    UserRole.SUPERADMIN.value,
    UserRole.ADMIN.value,
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _validate_password(
    password: str,
    *,
    required: bool,
) -> None:
    if required and not password:
        raise ValueError("A senha é obrigatória.")

    if password and len(password) < 8:
        raise ValueError(
            "A senha deve ter pelo menos 8 caracteres."
        )


def _get_manager(
    session,
    actor_user_id: int,
) -> User:
    actor = session.get(User, actor_user_id)

    if actor is None or not actor.is_active:
        raise PermissionError(
            "Usuário responsável pela ação não está disponível."
        )

    if actor.role not in MANAGER_ROLES:
        raise PermissionError(
            "Seu perfil não possui permissão para gerenciar usuários."
        )

    return actor


def _active_superadmin_count(session) -> int:
    users = session.exec(
        select(User).where(
            User.role == UserRole.SUPERADMIN.value,
            User.is_active == True,  # noqa: E712
        )
    ).all()

    return len(users)


def _revoke_user_sessions(
    session,
    user_id: int,
) -> None:
    sessions = session.exec(
        select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.revoked_at.is_(None),
        )
    ).all()

    now = _utc_now()

    for session_record in sessions:
        session_record.revoked_at = now
        session.add(session_record)


def _revoke_other_user_sessions(
    session,
    user_id: int,
    current_session_token: str,
) -> None:
    """
    Revoga todas as sessões do usuário, exceto
    a sessão atual usada para trocar a senha.
    """

    if not current_session_token:
        raise PermissionError(
            "Sua sessão não é válida."
        )

    current_token_hash = hash_session_token(
        current_session_token
    )

    current_session = session.exec(
        select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.token_hash == current_token_hash,
            UserSession.revoked_at.is_(None),
        )
    ).first()

    if current_session is None:
        raise PermissionError(
            "Sua sessão não é válida."
        )

    sessions = session.exec(
        select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.revoked_at.is_(None),
        )
    ).all()

    now = _utc_now()

    for session_record in sessions:
        if session_record.token_hash == current_token_hash:
            continue

        session_record.revoked_at = now
        session.add(session_record)


def get_user_by_id(
    user_id: int,
) -> User | None:
    with rx.session() as session:
        return session.get(User, user_id)


def get_user_by_email(
    email: str,
) -> User | None:
    normalized_email = validate_allowed_email(email)

    if not normalized_email:
        return None

    with rx.session() as session:
        return session.exec(
            select(User).where(
                User.email == normalized_email
            )
        ).first()


def create_user(
    name: str,
    email: str,
    password: str,
    role: str = UserRole.USER.value,
) -> int:
    """Criação interna, utilizada por seed/scripts."""

    normalized_name = name.strip()
    normalized_email = validate_allowed_email(email)
    normalized_role = normalize_role(role)

    if not normalized_name:
        raise ValueError("O nome é obrigatório.")

    if not normalized_email:
        raise ValueError("O e-mail é obrigatório.")

    _validate_password(password, required=True)

    with rx.session() as session:
        existing_user = session.exec(
            select(User).where(
                User.email == normalized_email
            )
        ).first()

        if existing_user:
            raise ValueError(
                "Já existe um usuário cadastrado com este e-mail."
            )

        user = User(
            name=normalized_name,
            email=normalized_email,
            password_hash=hash_password(password),
            role=normalized_role,
            is_active=True,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        if user.id is None:
            raise RuntimeError(
                "Não foi possível identificar o usuário criado."
            )

        return user.id


def list_users_for_management(
    actor_user_id: int,
) -> list[User]:
    """Lista usuários somente para Admin/SuperAdmin."""

    with rx.session() as session:
        _get_manager(session, actor_user_id)

        return list(
            session.exec(
                select(User).order_by(
                    User.name,
                    User.email,
                )
            ).all()
        )


def create_managed_user(
    actor_user_id: int,
    name: str,
    email: str,
    password: str,
    role: str,
    is_active: bool = True,
) -> int:
    """Cria usuário aplicando as regras de RBAC."""

    normalized_name = name.strip()
    normalized_email = validate_allowed_email(email)
    normalized_role = normalize_role(role)

    if not normalized_name:
        raise ValueError("O nome é obrigatório.")

    if not normalized_email:
        raise ValueError("O e-mail é obrigatório.")

    _validate_password(password, required=True)

    with rx.session() as session:
        actor = _get_manager(session, actor_user_id)

        if (
            normalized_role == UserRole.SUPERADMIN.value
            and actor.role != UserRole.SUPERADMIN.value
        ):
            raise PermissionError(
                "Somente um SuperAdmin pode criar outro SuperAdmin."
            )

        existing_user = session.exec(
            select(User).where(
                User.email == normalized_email
            )
        ).first()

        if existing_user:
            raise ValueError(
                "Já existe um usuário cadastrado com este e-mail."
            )

        user = User(
            name=normalized_name,
            email=normalized_email,
            password_hash=hash_password(password),
            role=normalized_role,
            is_active=is_active,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        if user.id is None:
            raise RuntimeError(
                "Não foi possível identificar o usuário criado."
            )

        return user.id


def update_managed_user(
    actor_user_id: int,
    target_user_id: int,
    name: str,
    email: str,
    role: str,
    is_active: bool,
    password: str = "",
) -> None:
    """Atualiza usuário aplicando as regras de segurança."""

    normalized_name = name.strip()
    normalized_email = validate_allowed_email(email)
    normalized_role = normalize_role(role)
    normalized_password = password.strip()

    if not normalized_name:
        raise ValueError("O nome é obrigatório.")

    if not normalized_email:
        raise ValueError("O e-mail é obrigatório.")

    _validate_password(normalized_password, required=False)

    with rx.session() as session:
        actor = _get_manager(session, actor_user_id)
        target = session.get(User, target_user_id)

        if target is None:
            raise ValueError("Usuário não encontrado.")

        if actor.id == target.id:
            raise ValueError(
                "Sua própria conta deve ser alterada pelo menu Perfil."
            )

        if (
            target.role == UserRole.SUPERADMIN.value
            and actor.role != UserRole.SUPERADMIN.value
        ):
            raise PermissionError(
                "Admin não pode alterar uma conta SuperAdmin."
            )

        if (
            normalized_role == UserRole.SUPERADMIN.value
            and actor.role != UserRole.SUPERADMIN.value
        ):
            raise PermissionError(
                "Somente um SuperAdmin pode conceder esse perfil."
            )

        existing_email = session.exec(
            select(User).where(
                User.email == normalized_email
            )
        ).first()

        if existing_email is not None and existing_email.id != target.id:
            raise ValueError(
                "Já existe um usuário cadastrado com este e-mail."
            )

        removes_active_superadmin = (
            target.role == UserRole.SUPERADMIN.value
            and target.is_active
            and (
                normalized_role != UserRole.SUPERADMIN.value
                or not is_active
            )
        )

        if removes_active_superadmin and _active_superadmin_count(session) <= 1:
            raise ValueError(
                "O sistema precisa manter pelo menos um SuperAdmin ativo."
            )

        role_changed = target.role != normalized_role
        status_changed = target.is_active != is_active
        password_changed = bool(normalized_password)

        target.name = normalized_name
        target.email = normalized_email
        target.role = normalized_role
        target.is_active = is_active

        if password_changed:
            target.password_hash = hash_password(normalized_password)

        session.add(target)

        if role_changed or status_changed or password_changed:
            _revoke_user_sessions(session, target_user_id)

        session.commit()


def change_own_password(
    *,
    user_id: int,
    current_password: str,
    new_password: str,
    current_session_token: str,
) -> None:
    """
    Altera a senha da própria conta.

    A sessão atual é preservada e todas as demais
    sessões ativas do usuário são revogadas.
    """

    if not current_password:
        raise ValueError("Informe sua senha atual.")

    normalized_new_password = new_password.strip()
    _validate_password(normalized_new_password, required=True)

    with rx.session() as session:
        user = session.get(User, user_id)

        if user is None or not user.is_active:
            raise PermissionError(
                "Sua conta não está disponível."
            )

        if not verify_password(current_password, user.password_hash):
            raise ValueError("A senha atual está incorreta.")

        if verify_password(normalized_new_password, user.password_hash):
            raise ValueError(
                "A nova senha deve ser diferente da senha atual."
            )

        _revoke_other_user_sessions(
            session,
            user_id,
            current_session_token,
        )

        user.password_hash = hash_password(normalized_new_password)
        session.add(user)
        session.commit()


def delete_managed_user(
    actor_user_id: int,
    target_user_id: int,
) -> None:
    """Exclusão permanente, restrita ao SuperAdmin."""

    with rx.session() as session:
        actor = _get_manager(session, actor_user_id)

        if actor.role != UserRole.SUPERADMIN.value:
            raise PermissionError(
                "Somente um SuperAdmin pode excluir usuários."
            )

        target = session.get(User, target_user_id)

        if target is None:
            raise ValueError("Usuário não encontrado.")

        if actor.id == target.id:
            raise ValueError(
                "Você não pode excluir a própria conta."
            )

        if (
            target.role == UserRole.SUPERADMIN.value
            and target.is_active
            and _active_superadmin_count(session) <= 1
        ):
            raise ValueError(
                "O sistema precisa manter pelo menos um SuperAdmin ativo."
            )

        user_sessions = session.exec(
            select(UserSession).where(
                UserSession.user_id == target_user_id
            )
        ).all()

        for session_record in user_sessions:
            session.delete(session_record)

        session.delete(target)
        session.commit()


def authenticate_user(
    email: str,
    password: str,
) -> User | None:
    """Valida credenciais e retorna o usuário autenticado."""

    normalized_email = validate_allowed_email(email)

    if not normalized_email or not password:
        return None

    with rx.session() as session:
        user = session.exec(
            select(User).where(
                User.email == normalized_email
            )
        ).first()

        if user is None or not user.is_active:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user
