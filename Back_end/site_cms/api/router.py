from fastapi import (
    APIRouter,
    HTTPException,
)

from Back_end.site_cms.api.public_service import (
    get_public_home,
    get_public_meta,
    get_public_know_metas,
    get_public_overview,
    get_public_overview_budget,
    get_public_single_page,
    list_public_metas,
)


router = APIRouter(
    prefix="/api/site",
    tags=["Site CMS"],
)


@router.get("/home")
def home():
    return get_public_home()


@router.get("/sobre")
def about():
    content = get_public_single_page(
        "about",
        "about",
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Conteúdo Sobre não publicado.",
        )

    return content


@router.get("/historico")
def history():
    content = get_public_single_page(
        "history",
        "history",
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Histórico não publicado.",
        )

    return content


@router.get("/regionalizacao")
def regionalization():
    content = get_public_single_page(
        "regionalization",
        "regionalization",
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Regionalização não publicada.",
        )

    return content


@router.get("/transparencia")
def transparency():
    content = get_public_single_page(
        "transparency",
        "transparency",
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Transparência não publicada.",
        )

    return content


@router.get("/metas")
def metas():
    return {
        "total": len(
            list_public_metas()
        ),
        "metas": (
            list_public_metas()
        ),
    }


@router.get("/metas/{codigo}")
def meta_detail(
    codigo: str,
):
    content = get_public_meta(
        codigo
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Meta não encontrada ou não publicada.",
        )

    return content


@router.get("/visao-geral")
def overview():
    content = (
        get_public_overview()
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Visão Geral não publicada.",
        )

    return content


# ------------------------------------------------------------
# ALIASES COMPATÍVEIS COM A DIVISÃO DA API ANTIGA
# ------------------------------------------------------------

@router.get(
    "/visao-geral/orcamento-geral"
)
def overview_budget():
    content = (
        get_public_overview_budget()
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Orçamento Geral não publicado.",
        )

    return content


@router.get(
    "/visao-geral/conheca-metas"
)
def overview_know_metas():
    content = (
        get_public_know_metas()
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Conheça Metas não publicado.",
        )

    return content
