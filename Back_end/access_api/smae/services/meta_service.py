import httpx

from copy import deepcopy
from typing import Any

from Back_end.access_api.smae.client import SmaeClient
from Back_end.access_api.smae.config import get_smae_config


def _extract_lines( response: dict, endpoint: str,) -> list[dict]:
    """Extrai o campo 'linhas' de uma resposta do SMAE."""

    linhas = response.get("linhas")

    if not isinstance(linhas, list):
        raise RuntimeError(
            f"Resposta inesperada do SMAE em {endpoint}: "
            "campo 'linhas' não encontrado."
        )

    return linhas


def _sanitize_meta_payload(meta: dict) -> dict:
    """
    Remove tokens de download que não fazem parte dos dados da meta.

    Mantém IDs, descrições e demais informações necessárias para
    persistência e exibição.
    """

    sanitized = deepcopy(meta)

    tags = sanitized.get("tags") or []

    for tag in tags:
        if isinstance(tag, dict):
            tag.pop("download_token", None)

    return sanitized


def fetch_metas() -> list[dict]:
    """
    Busca a listagem das metas do Programa de Metas configurado.

    Essa rota é adequada para catálogo e sincronização inicial.
    """

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

    linhas = _extract_lines(
        response,
        "/meta",
    )

    return [
        _sanitize_meta_payload(meta)
        for meta in linhas
    ]


def fetch_meta_detail( smae_id: int,) -> dict:
    """
    Busca os dados completos de uma meta pelo ID interno do SMAE.

    Exemplo:
        código da meta: 001
        ID SMAE: 1486
        endpoint: /meta/1486
    """

    config = get_smae_config()
    client = SmaeClient(config)

    try:
        response = client.get(
            f"/meta/{smae_id}"
        )
    finally:
        client.close()

    if not isinstance(response, dict):
        raise RuntimeError(
            f"Resposta inesperada do SMAE para a meta {smae_id}."
        )

    return _sanitize_meta_payload(response)


def fetch_iniciativas_atividades( meta_ids: list[int],) -> list[dict]:
    """
    Busca iniciativas e atividades vinculadas às metas.

    Os IDs são enviados em lotes para evitar uma URL excessivamente longa.
    """

    if not meta_ids:
        return []

    config = get_smae_config()
    client = SmaeClient(config)

    linhas: list[dict] = []

    try:
        batch_size = 50

        for start in range(
            0,
            len(meta_ids),
            batch_size,
        ):
            batch = meta_ids[
                start:start + batch_size
            ]

            response = client.get(
                "/meta/iniciativas-atividades",
                params={
                    "meta_ids": [
                        str(meta_id)
                        for meta_id in batch
                    ]
                },
            )

            linhas.extend(
                _extract_lines(
                    response,
                    "/meta/iniciativas-atividades",
                )
            )
    finally:
        client.close()

    return linhas


def fetch_relacionados( *, pdm_id: int | None = None, meta_id: int | None = None, iniciativa_id: int | None = None, atividade_id: int | None = None,) -> dict:
    """
    Busca metas, obras e projetos relacionados no SMAE.

    Se o SMAE responder 404, retorna uma estrutura vazia
    em vez de interromper a coleta da meta.
    """

    config = get_smae_config()

    params: dict[str, int] = {
        "pdm_id": pdm_id or config.pdm_id,
    }

    if meta_id is not None:
        params["meta_id"] = meta_id

    if iniciativa_id is not None:
        params["iniciativa_id"] = iniciativa_id

    if atividade_id is not None:
        params["atividade_id"] = atividade_id

    client = SmaeClient(config)

    try:
        try:
            return client.get(
                "/metas/relacinados",
                params=params,
            )

        except httpx.HTTPStatusError as error:
            if error.response.status_code == 404:
                return {
                    "metas": [],
                    "obras": [],
                    "projetos": [],
                }

            raise

    finally:
        client.close()


def fetch_meta_full_context( smae_id: int,) -> dict[str, Any]:
    """
    Busca todo o contexto conhecido de uma única meta.

    Útil para a futura Ficha da Meta.
    """

    meta = fetch_meta_detail(smae_id)

    iniciativas_atividades = (
        fetch_iniciativas_atividades(
            [smae_id]
        )
    )

    relacionados = fetch_relacionados(
        meta_id=smae_id
    )

    return {
        "meta": meta,
        "iniciativas_atividades": iniciativas_atividades,
        "relacionados": relacionados,
    }


def fetch_pdm_full_snapshot() -> dict[str, Any]:
    """
    Busca um retrato completo do PDM configurado.

    Reutiliza uma única sessão autenticada para buscar os detalhes
    das metas, evitando realizar um novo login para cada registro.
    """

    config = get_smae_config()
    client = SmaeClient(config)

    try:
        # 1. Catálogo geral das metas.
        metas_response = client.get(
            "/meta",
            params={
                "pdm_id": config.pdm_id,
            },
        )

        metas_resumo = _extract_lines(
            metas_response,
            "/meta",
        )

        meta_ids: list[int] = []

        for meta in metas_resumo:
            smae_id = meta.get("id")

            if not isinstance(smae_id, int):
                raise RuntimeError(
                    "Meta recebida do SMAE sem um ID válido."
                )

            meta_ids.append(smae_id)

        # 2. Detalhes completos de cada meta.
        metas_detalhes: list[dict] = []

        for smae_id in meta_ids:
            detail = client.get(
                f"/meta/{smae_id}"
            )

            metas_detalhes.append(
                _sanitize_meta_payload(detail)
            )

        # 3. Iniciativas e atividades.
        iniciativas_atividades: list[dict] = []

        batch_size = 50

        for start in range(
            0,
            len(meta_ids),
            batch_size,
        ):
            batch = meta_ids[
                start:start + batch_size
            ]

            response = client.get(
                "/meta/iniciativas-atividades",
                params={
                    "meta_ids": [
                        str(meta_id)
                        for meta_id in batch
                    ]
                },
            )

            iniciativas_atividades.extend(
                _extract_lines(
                    response,
                    "/meta/iniciativas-atividades",
                )
            )

        # 4. Relações do Programa de Metas.
        relacionados = client.get(
            "/metas/relacinados",
            params={
                "pdm_id": config.pdm_id,
            },
        )

    finally:
        client.close()

    return {
        "pdm_id": config.pdm_id,

        "metas_resumo": [
            _sanitize_meta_payload(meta)
            for meta in metas_resumo
        ],

        "metas_detalhes": metas_detalhes,

        "iniciativas_atividades": iniciativas_atividades,

        "relacionados": relacionados,
    }

def fetch_meta_details( smae_ids: list[int],) -> list[dict]:
    """
    Busca os detalhes completos de várias metas
    reutilizando uma única sessão autenticada no SMAE.
    """

    if not smae_ids:
        return []

    config = get_smae_config()
    client = SmaeClient(config)

    details: list[dict] = []

    try:
        for smae_id in smae_ids:
            response = client.get(
                f"/meta/{smae_id}"
            )

            if not isinstance(response, dict):
                raise RuntimeError(
                    f"Resposta inesperada do SMAE "
                    f"para a meta {smae_id}."
                )

            details.append(
                _sanitize_meta_payload(
                    response
                )
            )

    finally:
        client.close()

    return details