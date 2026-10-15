import reflex as rx

from sqlmodel import select
from Back_end.access.core.roles import (UserRole,normalize_role,)
from Back_end.access.core.security import (hash_password,verify_password,)
from Back_end.access.modules.users.model import (User,)

# ============================================================
# CONSULTAS
# ============================================================

def get_user_by_id(user_id: int,) -> User | None:
    """Busca um usuário pelo ID."""

    with rx.session() as session:
        return session.get(User,user_id,)


def get_user_by_email(email: str,) -> User | None:
    """Busca um usuário pelo e-mail."""
    normalized_email = (email.strip().lower())

    if not normalized_email:
        return None

    with rx.session() as session:
        return session.exec(select(User).where(User.email== normalized_email)).first()


# ============================================================
# CRIAÇÃO
# ============================================================

def create_user(name: str,email: str,password: str,role: str = UserRole.USER.value,) -> int:
    """Cria um novo usuário autorizado no sistema."""

    normalized_name = (name.strip())

    normalized_email = ( email.strip().lower() )

    normalized_role = normalize_role(role)

    if not normalized_name:
        raise ValueError("O nome é obrigatório.")

    if not normalized_email:
        raise ValueError("O e-mail é obrigatório.")

    if not password:
        raise ValueError("A senha é obrigatória.")

    with rx.session() as session:
        existing_user = session.exec(select(User).where(User.email== normalized_email)).first()
        if existing_user:
            raise ValueError(
                "Já existe um usuário "
                "cadastrado com este e-mail."
            )

        user = User(
            name=normalized_name,
            email=normalized_email,
            password_hash=(hash_password(password)),
            role=normalized_role,
            is_active=True,
        )

        session.add(user)

        session.commit()
        session.refresh(user)

        if user.id is None:
            raise RuntimeError("Não foi possível identificar " "o usuário criado.")

        return user.id


# ============================================================
# AUTENTICAÇÃO
# ============================================================

def authenticate_user(email: str,password: str,) -> User | None:
    """
    Valida credenciais e retorna
    o usuário autenticado.
    """

    normalized_email = (email.strip().lower())

    if (not normalized_email or not password):
        return None

    with rx.session() as session:
        user = session.exec(select(User).where(User.email== normalized_email)).first()
        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(password,user.password_hash,):
            return None

        return user