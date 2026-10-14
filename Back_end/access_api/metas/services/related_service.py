import reflex as rx

from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.smae.services.meta_service import (
    fetch_relacionados_by_meta_ids,
)


def diagnose_related_data() -> dict:
    """
    Analisa os relacionados das metas existentes no banco.

    Não persiste nada.
    Apenas coleta estatísticas para definirmos
    corretamente a estrutura de dados.
    """

    with rx.session() as session:
        metas = session.exec( select(Meta).order_by( Meta.smae_id ) ).all()
        meta_ids = [ meta.smae_id for meta in metas if meta.smae_id is not None ]

    relacionados_por_meta = ( fetch_relacionados_by_meta_ids( meta_ids) )

    metas_com_obras = 0
    metas_com_projetos = 0
    metas_com_metas_relacionadas = 0

    obras_unicas: dict[int, dict] = {}
    projetos_unicos: dict[int, dict] = {}
    subprefeituras_unicas: dict[int, dict] = {}

    for relacionados in ( relacionados_por_meta.values() ):
        obras = relacionados.get( "obras" ) or []
        projetos = relacionados.get( "projetos" ) or []
        metas_relacionadas = relacionados.get( "metas" ) or []
        if obras:
            metas_com_obras += 1

        if projetos:
            metas_com_projetos += 1

        if metas_relacionadas:
            metas_com_metas_relacionadas += 1

        for obra in obras:
            obra_id = obra.get("id")

            if isinstance( obra_id, int, ):
                obras_unicas[ obra_id ] = obra

            subprefeituras = ( obra.get( "subprefeituras" ) or [] )

            for subprefeitura in subprefeituras:
                subprefeitura_id = (subprefeitura.get("id") )

                if isinstance( subprefeitura_id, int, ):
                    subprefeituras_unicas[ subprefeitura_id ] = subprefeitura

        for projeto in projetos:
            projeto_id = projeto.get("id")

            if isinstance( projeto_id, int, ):
                projetos_unicos[ projeto_id ] = projeto

    return {
        "metas_analisadas": len(relacionados_por_meta),
        "metas_com_obras": (metas_com_obras),
        "metas_com_projetos": (metas_com_projetos),
        "metas_com_metas_relacionadas": (metas_com_metas_relacionadas),
        "obras_unicas": len(obras_unicas),
        "projetos_unicos": len(projetos_unicos),
        "subprefeituras_unicas": sorted( subprefeituras_unicas.values(),
            key=lambda item: ( item.get( "descricao", "", ).casefold() ),
        ),
    }