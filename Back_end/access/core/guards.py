from Back_end.access.core.permissions import (Permission,has_permission,)


def can_access(role: str | None,permission: str | Permission,) -> bool:
    """
    Verifica se determinado perfil pode
    acessar uma funcionalidade do sistema.

    Este helper mantém a autorização
    desacoplada da interface Reflex.
    """

    return has_permission(role,permission,)