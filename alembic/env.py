import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool
from sqlmodel import SQLModel

# Importa os models para registrá-los no metadata do SQLModel.
from Back_end.access.modules.auth.model import UserSession
from Back_end.access.modules.users.model import User
from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orcamento import MetaOrcamento

from Back_end.access_api.metas.models.tag import Tag
from Back_end.access_api.metas.models.meta_tag import MetaTag

from Back_end.access_api.metas.models.orgao import Orgao
from Back_end.access_api.metas.models.meta_orgao import MetaOrgao
from Back_end.access_api.metas.models.pessoa import Pessoa
from Back_end.access_api.metas.models.iniciativa import Iniciativa

from Back_end.access_api.metas.models.meta_pessoa import MetaPessoa
from Back_end.access_api.metas.models.meta_equipe import MetaEquipe


# Carrega as variáveis definidas no arquivo .env.
load_dotenv()


# Objeto de configuração do Alembic.
config = context.config


# Configuração de logs do Alembic.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# O autogenerate compara o banco com todos os models registrados
# no metadata do SQLModel.
target_metadata = SQLModel.metadata


def get_database_url() -> str:
    """Retorna a URL síncrona do PostgreSQL usada pelo projeto."""

    database_url = os.getenv("REFLEX_DB_URL")

    if not database_url:
        raise RuntimeError(
            "REFLEX_DB_URL não foi encontrada no arquivo .env."
        )

    return database_url


def run_migrations_offline() -> None:
    """Executa migrations sem abrir conexão direta com o banco."""

    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrations conectado ao PostgreSQL."""

    connectable = create_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()