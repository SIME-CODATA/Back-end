import os
from typing import Any

import reflex as rx
from Back_end.access.core.guards import (can_access,)
from Back_end.access.core.permissions import (Permission,)
from Back_end.access.core.roles import (UserRole,get_role_label,)
from Back_end.access.modules.audit.service import (create_audit_log,)
from Back_end.access.modules.auth.service import (create_session,revoke_session,validate_session,)
from Back_end.access.modules.users.service import (authenticate_user,get_user_by_id,)

SESSION_MAX_AGE = (8 * 60 * 60)


def _env_bool(
    name: str,
    default: bool = False,
) -> bool:
    """Lê uma variável de ambiente booleana."""
    value = os.getenv(
        name,
        str(default),
    )

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
        "sim",
    }


SESSION_COOKIE_SECURE = _env_bool(
    "SESSION_COOKIE_SECURE",
    False,
)


class AuthState(rx.State):
    """Controla autenticação, sessão e autorização."""
    # ========================================================
    # LOGIN
    # ========================================================
    error_message: str = ""

    # ========================================================
    # COOKIE
    # ========================================================

    session_token: str = rx.Cookie(
        "",
        name="pdm_session",
        path="/",
        max_age=SESSION_MAX_AGE,
        same_site="strict",

        # false no desenvolvimento local (HTTP)
        # true no ambiente publicado (HTTPS)
        secure=SESSION_COOKIE_SECURE,
    )

    # ========================================================
    # USUÁRIO AUTENTICADO
    # ========================================================

    current_user_id: int | None = None
    current_user_name: str = ""
    current_user_email: str = ""
    current_user_role: str = ""

    # ========================================================
    # INFORMAÇÕES DERIVADAS
    # ========================================================

    @rx.var
    def is_authenticated(self,) -> bool:
        """Indica se existe usuário autenticado."""
        return (self.current_user_id is not None)

    @rx.var
    def current_role_label(self,) -> str:
        """Retorna o nome amigável do perfil."""
        return get_role_label(self.current_user_role)

    @rx.var
    def is_superadmin(self,) -> bool:
        return (self.current_user_role== UserRole.SUPERADMIN.value)

    @rx.var
    def is_admin(self,) -> bool:
        return (self.current_user_role== UserRole.ADMIN.value)

    @rx.var
    def is_user(self,) -> bool:
        return (self.current_user_role== UserRole.USER.value)

    @rx.var
    def is_visitante(self,) -> bool:
        return (self.current_user_role== UserRole.VISITANTE.value)

    # ========================================================
    # PERMISSÕES PARA A INTERFACE
    # ========================================================

    @rx.var
    def can_view_dashboard(self,) -> bool:
        return can_access(self.current_user_role,Permission.DASHBOARD_VIEW,)

    @rx.var
    def can_view_metas(self,) -> bool:
        return can_access(self.current_user_role,Permission.METAS_VIEW,)

    @rx.var
    def can_view_site(self,) -> bool:
        return can_access(self.current_user_role,Permission.SITE_VIEW,)

    @rx.var
    def can_manage_users(self,) -> bool:
        return can_access( self.current_user_role, Permission.USERS_VIEW, )


    @rx.var
    def can_view_media(self,) -> bool:
        return can_access( self.current_user_role, Permission.MEDIA_VIEW, )

    @rx.var
    def can_view_audit(self,) -> bool:
        return can_access(self.current_user_role,Permission.AUDIT_VIEW,)

    @rx.var
    def can_manage_scheduler(self,) -> bool:
        return can_access( self.current_user_role, Permission.SCHEDULER_MANAGE, )

    @rx.var
    def can_manage_database(self,) -> bool:
        return can_access(self.current_user_role,Permission.DATABASE_VIEW,)
    
    @rx.var
    def can_sync_smae(self,) -> bool:
        """Indica se o usuário pode sincronizar dados do SMAE."""
        return can_access( self.current_user_role, Permission.SMAE_SYNC,)

    # ========================================================
    # USUÁRIO ATUAL
    # ========================================================

    def _clear_current_user(self,):
        """Remove os dados do usuário do State."""
        self.current_user_id = None
        self.current_user_name = ""
        self.current_user_email = ""
        self.current_user_role = ""

    def _set_current_user(self,user,):
        """Carrega o usuário no State."""
        self.current_user_id = (user.id)
        self.current_user_name = (user.name)
        self.current_user_email = (user.email)
        self.current_user_role = (user.role or UserRole.USER.value)

    def _audit(
        self,
        *,
        action: str,
        entity_type: str = "system",
        entity_id: str | int | None = None,
        description: str = "",
    ) -> None:
        """
        Registra auditoria usando o usuário autenticado como ator.

        Falha de auditoria não interrompe a ação principal.
        """
        try:
            create_audit_log(
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                description=description,
                actor_user_id=self.current_user_id,
                actor_name=self.current_user_name,
                actor_email=self.current_user_email,
                actor_role=self.current_user_role,
            )

        except Exception as error:
            print(
                "Erro ao registrar auditoria: "
                f"{error}"
            )

    # ========================================================
    # RESTAURAÇÃO DA SESSÃO
    # ========================================================

    def _restore_authenticated_user(self,):
        """
        Valida a sessão e carrega novamente
        o usuário a partir do banco.

        Isso garante que alterações de papel,
        bloqueios de conta etc. passem a valer
        sem depender da expiração do cookie.
        """

        user_id = validate_session(self.session_token)

        # ----------------------------------------------------
        # SESSÃO INVÁLIDA / EXPIRADA
        # ----------------------------------------------------

        if user_id is None:
            self.session_token = ""
            self._clear_current_user()
            return None

        # ----------------------------------------------------
        # BUSCA USUÁRIO
        # ----------------------------------------------------

        user = get_user_by_id(user_id)

        # ----------------------------------------------------
        # USUÁRIO NÃO EXISTE / BLOQUEADO
        # ----------------------------------------------------

        if (user is None or not user.is_active):
            if self.session_token:
                revoke_session(self.session_token)
                
            self.session_token = ""
            self._clear_current_user()
            return None

        # ----------------------------------------------------
        # CARREGA O USUÁRIO ATUALIZADO
        # ----------------------------------------------------

        self._set_current_user(user)
        return user

    # ========================================================
    # AUTORIZAÇÃO
    # ========================================================

    def _require_permission( self, permission: Permission,):
        """
        Verifica autenticação e autorização.
        Sem sessão:
            /login
        Com sessão, mas sem permissão:
            /403
        """
        user = (self._restore_authenticated_user())
        if user is None:
            return rx.redirect("/login")

        if not can_access(self.current_user_role,permission,):
            return rx.redirect("/403")

        return None

    # ========================================================
    # LOGIN
    # ========================================================

    @rx.event
    def login(self,form_data: dict[str,Any,],):
        """Autentica o usuário e cria uma sessão."""

        self.error_message = ""

        email = str(form_data.get("email","",)).strip()
        password = str(form_data.get("password","",))
        user = authenticate_user(email=email,password=password,)

        if (user is None or user.id is None):
            self.error_message = ( "E-mail ou senha inválidos.")
            return

        token = create_session(user.id)
        self.session_token = token
        self._set_current_user(user)

        self._audit(
            action="LOGIN",
            entity_type="authentication",
            entity_id=user.id,
            description="Login realizado com sucesso.",
        )

        # Primeiro envia o cookie.
        yield

        # Depois navega.
        yield rx.redirect("/admin")

    # ========================================================
    # AUTENTICAÇÃO SIMPLES
    # ========================================================

    @rx.event
    def require_auth(self,):
        """
        Exige somente que exista
        uma sessão autenticada.
        """

        user = (self._restore_authenticated_user())

        if user is None:
            return rx.redirect("/login")

    # ========================================================
    # GUARDS POR MÓDULO
    # ========================================================

    @rx.event
    def require_dashboard_access(self,):
        """Protege o painel geral."""
        return self._require_permission(Permission.DASHBOARD_VIEW)


    @rx.event
    def require_metas_access(self,):
        """Protege as páginas de metas."""
        return self._require_permission(Permission.METAS_VIEW)

    @rx.event
    def require_site_access(self,):
        """Protege o futuro módulo Site."""
        return self._require_permission(Permission.SITE_VIEW)

    @rx.event
    def require_users_access(self,):
        """Protege a administração de usuários."""
        return self._require_permission(Permission.USERS_VIEW)

    @rx.event
    def require_media_access(self,):
        """Protege o banco de imagens."""
        return self._require_permission(Permission.MEDIA_VIEW)

    @rx.event
    def require_audit_access(self,):
        """Protege auditoria e relatórios de acesso."""
        return self._require_permission(Permission.AUDIT_VIEW)

    @rx.event
    def require_scheduler_access(self,):
        """Protege os agendamentos SMAE."""
        return self._require_permission(Permission.SCHEDULER_VIEW)

    @rx.event
    def require_database_access(self,):
        """Protege administração do banco."""
        return self._require_permission(Permission.DATABASE_VIEW)

    # ========================================================
    # LOGOUT
    # ========================================================

    @rx.event
    def logout(self,):
        """Encerra a sessão atual."""
        if (
            self.current_user_id is None
            and self.session_token
        ):
            self._restore_authenticated_user()

        if self.current_user_id is not None:
            self._audit(
                action="LOGOUT",
                entity_type="authentication",
                entity_id=self.current_user_id,
                description="Logout realizado com sucesso.",
            )


    @rx.event
    def require_metas_access(self,):
        """Protege as páginas de metas."""
        return self._require_permission(Permission.METAS_VIEW)

    @rx.event
    def require_site_access(self,):
        """Protege o futuro módulo Site."""
        return self._require_permission(Permission.SITE_VIEW)

    @rx.event
    def require_users_access(self,):
        """Protege a administração de usuários."""
        return self._require_permission(Permission.USERS_VIEW)

    @rx.event
    def require_media_access(self,):
        """Protege o banco de imagens."""
        return self._require_permission(Permission.MEDIA_VIEW)

    @rx.event
    def require_audit_access(self,):
        """Protege auditoria e relatórios de acesso."""
        return self._require_permission(Permission.AUDIT_VIEW)

    @rx.event
    def require_scheduler_access(self,):
        """Protege os agendamentos SMAE."""
        return self._require_permission(Permission.SCHEDULER_VIEW)

    @rx.event
    def require_database_access(self,):
        """Protege administração do banco."""
        return self._require_permission(Permission.DATABASE_VIEW)

    # ========================================================
    # LOGOUT
    # ========================================================

    @rx.event
    def logout(self,):
        """Encerra a sessão atual."""
        if self.session_token:
            revoke_session(self.session_token)

        self.session_token = ""
        self._clear_current_user()
        yield rx.remove_cookie("pdm_session")
        yield rx.redirect("/login")