from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Usuário autorizado a acessar o painel administrativo."""

    __tablename__ = "users"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str

    email: str = Field(
        index=True,
        unique=True,
    )

    password_hash: str

    is_active: bool = Field(
        default=True,
    )