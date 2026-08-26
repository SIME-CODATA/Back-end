from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Gera um hash seguro para armazenamento da senha."""

    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se uma senha corresponde ao hash armazenado."""

    return password_hash.verify(
        password,
        hashed_password,
    )