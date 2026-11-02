from fastapi import APIRouter, HTTPException

from Back_end.site_cms.api.meta_public_service import (
    get_public_filter_options,
    get_public_map,
    get_public_meta_detail,
    get_public_meta_map,
    list_public_meta_cards,
    search_public_metas,
)
from Back_end.site_cms.api.meta_schemas import MetaSearchRequest


router = APIRouter(
    prefix="/api/site/metas",
    tags=["Site CMS - Metas"],
)


@router.get("")
def meta_list():
    metas = list_public_meta_cards()
    return {
        "total": len(metas),
        "metas": metas,
    }


@router.post("/pesquisa")
def meta_search(filters: MetaSearchRequest):
    return search_public_metas(filters)


@router.put(
    "/pesquisa",
    deprecated=True,
    summary="Alias compatível da pesquisa; prefira POST",
)
def meta_search_put(filters: MetaSearchRequest):
    return search_public_metas(filters)


@router.get("/filtros")
def meta_filters():
    return get_public_filter_options()


@router.get("/mapa")
def meta_map_all():
    return get_public_map()


@router.get("/{codigo}/mapa")
def meta_map(codigo: str):
    content = get_public_meta_map(codigo)
    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Meta não encontrada ou não publicada.",
        )
    return content


@router.get("/{codigo}")
def meta_detail(codigo: str):
    content = get_public_meta_detail(codigo)
    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Meta não encontrada ou não publicada.",
        )
    return content
