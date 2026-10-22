from datetime import datetime, timedelta, timezone

import reflex as rx
from sqlmodel import select

from Back_end.access.core.roles import (UserRole,get_role_label,)
from Back_end.access.modules.audit.model import AuditLog
from Back_end.access.modules.users.service import (change_own_password,)
from Back_end.access.states.auth_state import AuthState


ActivityRow = dict[str, str]

SAO_PAULO_TIMEZONE = timezone(timedelta(hours=-3))

ACTION_LABELS = {
    "LOGIN": "Login",
    "LOGOUT": "Logout",
    "USER_CREATED": "Usuário criado",
    "USER_UPDATED": "Usuário editado",
    "USER_ROLE_CHANGED": "Perfil alterado",
    "USER_DISABLED": "Usuário desativado",
    "USER_ENABLED": "Usuário ativado",
    "USER_DELETED": "Usuário excluído",
    "SMAE_SYNC": "SMAE atualizado",
    "SMAE_SYNC_FAILED": "Falha na atualização SMAE",
    "PASSWORD_CHANGED": "Senha alterada",
}

SYSTEM_UPDATE_ACTIONS = {
    "USER_CREATED",
    "USER_UPDATED",
    "USER_ROLE_CHANGED",
    "USER_DISABLED",
    "USER_ENABLED",
    "USER_DELETED",
    "SMAE_SYNC",
    "SMAE_SYNC_FAILED",
    "PASSWORD_CHANGED",
}


def _format_datetime(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    local_time = value.astimezone(SAO_PAULO_TIMEZONE)
    return local_time.strftime("%d/%m/%Y às %H:%M")


def _serialize_log(log: AuditLog) -> ActivityRow:
    action = str(log.action or "")

    return {
        "id": str(log.id or ""),
        "action": action,
        "action_label": ACTION_LABELS.get(
            action,
            action.replace("_", " ").title(),
        ),
        "description": str(log.description or ""),
        "created_at": _format_datetime(log.created_at),
        "actor_name": str(log.actor_name or "Sistema"),
        "actor_email": str(log.actor_email or ""),
    }


class ProfileState(rx.State):
    """Estado da página de perfil."""

    loading: bool = False

    profile_user_id: int | None = None
    profile_name: str = ""
    profile_email: str = ""
    profile_role: str = ""
    profile_role_label: str = ""

    activities: list[ActivityRow] = []
    system_updates: list[ActivityRow] = []

    profile_error_message: str = ""

    current_password: str = ""
    new_password: str = ""
    confirm_password: str = ""

    changing_password: bool = False
    password_error_message: str = ""
    password_success_message: str = ""

    @rx.var
    def has_activities(self) -> bool:
        return bool(self.activities)

    @rx.var
    def has_system_updates(self) -> bool:
        return bool(self.system_updates)

    @rx.var
    def show_system_updates(self) -> bool:
        return self.profile_role == UserRole.SUPERADMIN.value

    def _clear_password_form(self) -> None:
        self.current_password = ""
        self.new_password = ""
        self.confirm_password = ""

    def _load_logs(
        self,
        user_id: int,
        *,
        include_system_updates: bool,
    ) -> None:
        with rx.session() as session:
            personal_logs = list(
                session.exec(
                    select(AuditLog)
                    .where(AuditLog.actor_user_id == user_id)
                    .order_by(AuditLog.created_at.desc())
                    .limit(10)
                ).all()
            )

            self.activities = [
                _serialize_log(log)
                for log in personal_logs
            ]

            if not include_system_updates:
                self.system_updates = []
                return

            recent_logs = list(
                session.exec(
                    select(AuditLog)
                    .order_by(AuditLog.created_at.desc())
                    .limit(50)
                ).all()
            )

            updates = [
                log
                for log in recent_logs
                if log.action in SYSTEM_UPDATE_ACTIONS
            ][:10]

            self.system_updates = [
                _serialize_log(log)
                for log in updates
            ]

    @rx.event
    async def load_profile(self):
        self.loading = True
        self.profile_error_message = ""
        self.password_error_message = ""
        self.password_success_message = ""

        auth_state = await self.get_state(AuthState)

        try:
            user = auth_state._restore_authenticated_user()

            if user is None or user.id is None:
                yield rx.redirect("/login")
                return

            self.profile_user_id = user.id
            self.profile_name = user.name or ""
            self.profile_email = user.email or ""
            self.profile_role = user.role or UserRole.USER.value
            self.profile_role_label = get_role_label(self.profile_role)

            self._load_logs(
                user.id,
                include_system_updates=(
                    self.profile_role == UserRole.SUPERADMIN.value
                ),
            )

        except Exception as error:
            print(f"Erro ao carregar perfil: {error}")
            self.profile_error_message = (
                "Não foi possível carregar todas as informações do perfil."
            )

        finally:
            self.loading = False

    @rx.event
    def update_current_password(self, value: str):
        self.current_password = value
        self.password_error_message = ""
        self.password_success_message = ""

    @rx.event
    def update_new_password(self, value: str):
        self.new_password = value
        self.password_error_message = ""
        self.password_success_message = ""

    @rx.event
    def update_confirm_password(self, value: str):
        self.confirm_password = value
        self.password_error_message = ""
        self.password_success_message = ""

    @rx.event
    async def change_password(self):
        self.password_error_message = ""
        self.password_success_message = ""

        if self.new_password != self.confirm_password:
            self.password_error_message = (
                "A confirmação da nova senha não confere."
            )
            return

        self.changing_password = True
        yield

        auth_state = await self.get_state(AuthState)

        try:
            user = auth_state._restore_authenticated_user()

            if user is None or user.id is None:
                yield rx.redirect("/login")
                return

            change_own_password(
                user_id=user.id,
                current_password=self.current_password,
                new_password=self.new_password,
                current_session_token=auth_state.session_token,
            )

            auth_state._audit(
                action="PASSWORD_CHANGED",
                entity_type="user",
                entity_id=user.id,
                description="Senha da própria conta alterada com sucesso.",
            )

            self.password_success_message = (
                "Senha alterada com sucesso. "
                "As outras sessões da sua conta foram encerradas."
            )

            self._clear_password_form()

            self._load_logs(
                user.id,
                include_system_updates=(
                    user.role == UserRole.SUPERADMIN.value
                ),
            )

        except (ValueError, PermissionError) as error:
            self.password_error_message = str(error)

        except Exception as error:
            print(f"Erro ao alterar senha: {error}")
            self.password_error_message = (
                "Não foi possível alterar sua senha."
            )

        finally:
            self.changing_password = False
