from Back_end.smae.client import SmaeClient
from Back_end.smae.config import get_smae_config


def fetch_metas() -> list[dict]:
    """Busca as metas do Programa de Metas configurado."""

    config = get_smae_config()

    client = SmaeClient(config)

    try:
        response = client.get(
            "/meta",
            params={
                "pdm_id": config.pdm_id,
            },
        )
    finally:
        client.close()

    linhas = response.get("linhas")

    if not isinstance(linhas, list):
        raise RuntimeError(
            "Resposta inesperada do SMAE: campo 'linhas' não encontrado."
        )

    return linhas