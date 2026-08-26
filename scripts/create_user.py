from getpass import getpass

from Back_end.access.modules.users.service import create_user


def main() -> None:
    """Cria um usuário autorizado para acessar o sistema."""

    print("\n=== Programa de Metas V2.0 ===")
    print("Criação de usuário\n")

    name = input("Nome: ").strip()
    email = input("E-mail: ").strip()

    password = getpass("Senha: ")
    password_confirmation = getpass("Confirme a senha: ")

    if password != password_confirmation:
        print("\nErro: as senhas não coincidem.")
        return

    try:
        user_id = create_user(
            name=name,
            email=email,
            password=password,
        )

    except ValueError as error:
        print(f"\nErro: {error}")
        return

    print("\nUsuário criado com sucesso.")
    print(f"ID: {user_id}")


if __name__ == "__main__":
    main()