import reflex as rx
from sqlmodel import select

from Back_end.access.core.security import hash_password
from Back_end.access.modules.users.model import User
from Back_end.access.core.security import hash_password, verify_password


def create_user(
    name: str,
    email: str,
    password: str,
) -> int:
    """Cria um novo usuário autorizado no sistema."""

    normalized_name = name.strip()
    normalized_email = email.strip().lower()

    if not normalized_name:
        raise ValueError("O nome é obrigatório.")

    if not normalized_email:
        raise ValueError("O e-mail é obrigatório.")

    if not password:
        raise ValueError("A senha é obrigatória.")

    with rx.session() as session:
        existing_user = session.exec(
            select(User).where(User.email == normalized_email)
        ).first()

        if existing_user:
            raise ValueError(
                "Já existe um usuário cadastrado com este e-mail."
            )

        user = User(
            name=normalized_name,
            email=normalized_email,
            password_hash=hash_password(password),
            is_active=True,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        if user.id is None:
            raise RuntimeError("Não foi possível identificar o usuário criado.")

        return user.id

    
def authenticate_user(
    email: str,
    password: str,
) -> User | None:
    """Valida as credenciais e retorna o usuário autenticado."""

    normalized_email = email.strip().lower()

    if not normalized_email or not password:
        return None

    with rx.session() as session:
        user = session.exec(
            select(User).where(User.email == normalized_email)
        ).first()

        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user