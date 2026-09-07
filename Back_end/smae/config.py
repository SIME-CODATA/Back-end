import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class SmaeConfig:
    base_url: str
    email: str
    password: str
    systems: str
    pdm_id: int


def get_smae_config() -> SmaeConfig:
    """Carrega e valida as configurações necessárias para acessar o SMAE."""

    base_url = os.getenv("SMAE_BASE_URL", "").strip()
    email = os.getenv("SMAE_EMAIL", "").strip()
    password = os.getenv("SMAE_PASSWORD", "")
    systems = os.getenv("SMAE_SYSTEMS", "").strip()
    pdm_id = os.getenv("SMAE_PDM_ID", "").strip()

    if not base_url:
        raise RuntimeError("SMAE_BASE_URL não configurado.")

    if not email:
        raise RuntimeError("SMAE_EMAIL não configurado.")

    if not password:
        raise RuntimeError("SMAE_PASSWORD não configurado.")

    if not systems:
        raise RuntimeError("SMAE_SYSTEMS não configurado.")

    if not pdm_id:
        raise RuntimeError("SMAE_PDM_ID não configurado.")

    return SmaeConfig(
        base_url=base_url.rstrip("/"),
        email=email,
        password=password,
        systems=systems,
        pdm_id=int(pdm_id),
    )