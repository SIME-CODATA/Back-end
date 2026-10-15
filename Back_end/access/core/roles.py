from enum import Enum

class UserRole(str, Enum):
    """Papéis disponíveis no painel administrativo."""

    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    USER = "user"
    VISITANTE = "visitante"


ROLE_LABELS = {
    UserRole.SUPERADMIN.value: "SuperAdmin",
    UserRole.ADMIN.value: "Administrador",
    UserRole.USER.value: "Usuário",
    UserRole.VISITANTE.value: "Visitante",
}


def normalize_role(value: str | UserRole | None,) -> str:
    """
    Normaliza e valida um papel de usuário. Retorna sempre o valor utilizado no banco.
    """
    if isinstance(value, UserRole):
        return value.value

    normalized = str(value or "").strip().lower()
    valid_roles = {role.value for role in UserRole}

    if normalized not in valid_roles:
        raise ValueError(f"Perfil de acesso inválido: {value}")

    return normalized


def get_role_label(role: str | None,) -> str:
    """Retorna o nome amigável do papel."""
    return ROLE_LABELS.get(
        str(role or "").strip().lower(),
        "Usuário",
    )