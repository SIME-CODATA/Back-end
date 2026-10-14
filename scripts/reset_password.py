from getpass import getpass

import reflex as rx
from sqlalchemy import text

from Back_end.access.core.security import hash_password


def main() -> None:
    """Redefine a senha de um usuário existente."""

    print("\n=== Programa de Metas V2.0 ===")
    print("Redefinição de senha\n")

    email = input("E-mail do usuário: ").strip().lower()

    password = getpass("Nova senha: ")
    password_confirmation = getpass("Confirme a nova senha: ")

    if not password:
        print("\nErro: a senha não pode ficar vazia.")
        return

    if password != password_confirmation:
        print("\nErro: as senhas não coincidem.")
        return

    new_password_hash = hash_password(password)

    with rx.session() as session:
        user = session.execute(
            text(
                """
                SELECT id, name, email
                FROM users
                WHERE LOWER(email) = :email
                """
            ),
            {"email": email},
        ).first()

        if user is None:
            print("\nErro: usuário não encontrado.")
            return

        session.execute(
            text(
                """
                UPDATE users
                SET password_hash = :password_hash
                WHERE id = :user_id
                """
            ),
            {
                "password_hash": new_password_hash,
                "user_id": user.id,
            },
        )

        session.commit()

    print("\nSenha alterada com sucesso.")
    print(f"Usuário: {user.name}")
    print(f"E-mail: {user.email}")


if __name__ == "__main__":
    main()