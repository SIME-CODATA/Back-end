from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel
from Back_end.access.core.roles import (UserRole,)

class User(SQLModel, table=True):
    """Usuário autorizado a acessar o painel administrativo."""
    __tablename__ = "users"

    id: int | None = Field(default=None,primary_key=True,)
    name: str
    email: str = Field(index=True,unique=True,)
    password_hash: str
    role: str = Field(
        default=UserRole.USER.value,
        sa_column=Column(String(20),nullable=False,server_default=UserRole.USER.value,index=True,),
    )
    is_active: bool = Field(default=True,)