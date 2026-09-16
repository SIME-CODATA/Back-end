from fastapi import APIRouter

from Back_end.access_api.metas.services.query_service import list_metas


router = APIRouter(
    prefix="/api/metas",
    tags=["Metas"],
)


@router.get("")
def get_metas():
    """Lista as metas persistidas no PDM V2."""

    metas = list_metas()

    return {
        "linhas": [
            {
                "id": meta.id,
                "smae_id": meta.smae_id,
                "pdm_id": meta.pdm_id,
                "codigo": meta.codigo,
                "titulo": meta.titulo,
                "contexto": meta.contexto,
                "complemento": meta.complemento,
                "ativo": meta.ativo,
                "tema": {
                    "id": meta.tema_smae_id,
                    "descricao": meta.tema_descricao,
                }
                if meta.tema_smae_id is not None
                else None,
                "synced_at": meta.synced_at.isoformat(),
            }
            for meta in metas
        ]
    }