from enum import Enum
from Back_end.access.core.roles import (UserRole,normalize_role,)

class Permission(str, Enum):
    """Permissões disponíveis no sistema."""

    # ========================================================
    # PAINEL / VISÃO GERAL
    # ========================================================

    DASHBOARD_VIEW = "dashboard.view"
    DASHBOARD_SUMMARY = "dashboard.summary"
    DASHBOARD_DEADLINES = "dashboard.deadlines"
    DASHBOARD_BUDGET = "dashboard.budget"

    # ========================================================
    # METAS
    # ========================================================

    METAS_VIEW = "metas.view"

    # ========================================================
    # SITE / CMS
    # ========================================================

    SITE_VIEW = "site.view"
    SITE_ADD = "site.add"
    SITE_EDIT = "site.edit"
    SITE_CREATE = "site.create"
    SITE_DELETE = "site.delete"
    SITE_PUBLISH = "site.publish"

    # ========================================================
    # USUÁRIOS
    # ========================================================

    USERS_VIEW = "users.view"
    USERS_CREATE = "users.create"
    USERS_EDIT = "users.edit"
    USERS_EDIT_ACCESS = "users.edit_access"
    USERS_DELETE = "users.delete"

    # ========================================================
    # BANCO DE IMAGENS
    # ========================================================

    MEDIA_VIEW = "media.view"
    MEDIA_ADD = "media.add"
    MEDIA_EDIT = "media.edit"
    MEDIA_DELETE = "media.delete"

    # ========================================================
    # AUDITORIA
    # ========================================================

    AUDIT_VIEW = "audit.view"

    # ========================================================
    # BANCO DE DADOS
    # ========================================================

    DATABASE_VIEW = "database.view"
    DATABASE_BACKUP = "database.backup"
    DATABASE_RESTORE = "database.restore"

    # ========================================================
    # AGENDAMENTO
    # ========================================================

    SCHEDULER_VIEW = "scheduler.view"
    SCHEDULER_MANAGE = "scheduler.manage"
    
    # ========================================================
    # SMAE
    # ========================================================

    SMAE_SYNC = "smae.sync"


# ============================================================
# MATRIZ DE ACESSO
# ============================================================

ROLE_PERMISSIONS: dict[str, set[str]] = {

    # ========================================================
    # SUPERADMIN
    # ========================================================

    UserRole.SUPERADMIN.value: {
        permission.value
        for permission in Permission
    },

    # ========================================================
    # ADMIN
    # ========================================================

    UserRole.ADMIN.value: {
        Permission.DASHBOARD_VIEW.value,
        Permission.DASHBOARD_SUMMARY.value,
        Permission.DASHBOARD_DEADLINES.value,
        Permission.DASHBOARD_BUDGET.value,

        Permission.METAS_VIEW.value,

        Permission.SITE_VIEW.value,
        Permission.SITE_ADD.value,
        Permission.SITE_EDIT.value,
        Permission.SITE_CREATE.value,
        Permission.SITE_DELETE.value,
        Permission.SITE_PUBLISH.value,

        Permission.USERS_VIEW.value,
        Permission.USERS_CREATE.value,
        Permission.USERS_EDIT.value,
        Permission.USERS_EDIT_ACCESS.value,

        Permission.MEDIA_VIEW.value,
        Permission.MEDIA_ADD.value,
        Permission.MEDIA_EDIT.value,
        Permission.MEDIA_DELETE.value,
        
        Permission.SMAE_SYNC.value,
    },

    # ========================================================
    # USER
    # ========================================================

    UserRole.USER.value: {
        Permission.DASHBOARD_VIEW.value,
        Permission.DASHBOARD_SUMMARY.value,
        Permission.DASHBOARD_DEADLINES.value,

        Permission.METAS_VIEW.value,

        Permission.SITE_VIEW.value,
        Permission.SITE_ADD.value,
        Permission.SITE_EDIT.value,

        Permission.MEDIA_VIEW.value,
        Permission.MEDIA_ADD.value,
        Permission.MEDIA_EDIT.value,
        
        Permission.SMAE_SYNC.value,
    },

    # ========================================================
    # VISITANTE
    # ========================================================

    UserRole.VISITANTE.value: {Permission.DASHBOARD_VIEW.value,Permission.METAS_VIEW.value,},
}


def get_permissions(role: str | UserRole | None,) -> set[str]:
    """Retorna as permissões associadas a um perfil."""

    if not role:
        return set()

    try:
        normalized_role = normalize_role(role)

    except ValueError:
        return set()
    return set(
        ROLE_PERMISSIONS.get(normalized_role,set(),)
    )


def has_permission(role: str | UserRole | None,permission: str | Permission,) -> bool:
    """Verifica se um perfil possui determinada permissão."""

    permission_value = ( permission.value
        if isinstance(permission, Permission,)
        else str(permission)
    )

    return (permission_value in get_permissions(role))