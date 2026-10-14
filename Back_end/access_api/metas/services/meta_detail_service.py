import reflex as rx

from sqlmodel import select
from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_orcamento import ( MetaOrcamento,)
from Back_end.access_api.metas.models.meta_orgao import ( MetaOrgao,)
from Back_end.access_api.metas.models.orgao import ( Orgao,)
from Back_end.access_api.metas.models.meta_tag import ( MetaTag,)
from Back_end.access_api.metas.models.tag import (Tag,)
from Back_end.access_api.metas.models.iniciativa import (Iniciativa,)
from Back_end.access_api.metas.services.classification_service import (classify_meta_tags,)
from Back_end.access_api.smae.services.meta_service import (fetch_relacionados,)

# ============================================================
# CONFIGURAÇÃO TERRITORIAL
# ============================================================

REGIOES_POR_PARENTE_ID = {
    181: "Zona Leste",
    182: "Zona Norte",
    183: "Zona Sul",
    184: "Zona Oeste",
    185: "Centro",
}


# ============================================================
# HELPERS
# ============================================================

def _format_money(value,) -> str | None:
    """Formata um valor monetário no padrão brasileiro."""
    if value is None:
        return None

    formatted = (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {formatted}"


# ============================================================
# FICHA DA META
# ============================================================

def get_meta_detail_by_codigo(codigo: str,) -> dict | None:
    """
    Monta a Ficha da Meta combinando dados locais
    com dados relacionados obtidos no SMAE.

    Retorna None quando o código não existe.
    """

    with rx.session() as session:

        # ====================================================
        # META
        # ====================================================

        meta = session.exec(select(Meta).where(Meta.codigo == codigo)).first()
        if meta is None:
            return None
        if meta.id is None:
            raise RuntimeError(f"Meta {codigo} sem ID local.")

        # ====================================================
        # NAVEGAÇÃO ENTRE METAS
        # ====================================================

        codigos_metas = session.exec(select(Meta.codigo).order_by(Meta.codigo)).all()

        codigo_anterior = ""
        codigo_proximo = ""

        try:
            indice_atual = codigos_metas.index(meta.codigo)
            if indice_atual > 0:
                codigo_anterior = (codigos_metas[indice_atual - 1])
            if (indice_atual< len(codigos_metas) - 1):
                codigo_proximo = (codigos_metas[indice_atual + 1])

        except ValueError:
            pass

        # ====================================================
        # TAGS E CLASSIFICAÇÃO
        # ====================================================

        tags = session.exec(select(Tag).join(MetaTag,MetaTag.tag_id == Tag.id,).where(MetaTag.meta_id == meta.id).order_by(Tag.descricao)).all()
        
        tag_descriptions = {tag.descricao for tag in tags}

        classification = classify_meta_tags(
            meta_id=meta.id,
            codigo=meta.codigo,
            descriptions=tag_descriptions,
        )

        ods = [ tag.descricao for tag in tags
            if tag.descricao.startswith( "ODS ")
        ]

        todas_tags = [tag.descricao for tag in tags]

        # ====================================================
        # ÓRGÃOS
        # ====================================================

        orgao_rows = session.exec( select(Orgao.sigla,Orgao.descricao,MetaOrgao.responsavel,) .join(MetaOrgao,MetaOrgao.orgao_id == Orgao.id,) .where(MetaOrgao.meta_id == meta.id) .order_by(Orgao.sigla)).all()

        orgaos = [
            {
                "sigla": sigla or "",
                "descricao": descricao,
                "responsavel": responsavel,
            }
            for (
                sigla,
                descricao,
                responsavel,
            ) in orgao_rows
        ]

        # ====================================================
        # ORÇAMENTO
        # ====================================================

        orcamento = session.exec(
            select(
                MetaOrcamento
            ).where(
                MetaOrcamento.meta_id
                == meta.id
            )
        ).first()

        orcamento_data = None

        if orcamento is not None:
            orcamento_data = {
                "previsao": _format_money(
                    orcamento.total_previsao
                ),

                "empenhado": _format_money(
                    orcamento.total_empenhado
                ),

                "liquidado": _format_money(
                    orcamento.total_liquidado
                ),

                "atualizado_em": (
                    orcamento.atualizado_em.isoformat()
                    if (
                        orcamento.atualizado_em
                        is not None
                    )
                    else None
                ),
            }

        # ====================================================
        # INICIATIVAS
        # ====================================================

        iniciativas = session.exec(
            select(Iniciativa)
            .where(
                Iniciativa.meta_id == meta.id
            )
            .order_by(
                Iniciativa.codigo
            )
        ).all()

        iniciativas_data = [
            {
                "codigo": iniciativa.codigo,
                "titulo": iniciativa.titulo,
            }
            for iniciativa in iniciativas
        ]

        # ====================================================
        # RELACIONADOS SMAE
        # ====================================================

        relacionados = {
            "metas": [],
            "obras": [],
            "projetos": [],
        }

        if meta.smae_id is not None:
            try:
                relacionados = (
                    fetch_relacionados(
                        meta_id=meta.smae_id
                    )
                )

            except Exception as error:
                print(
                    "Erro ao carregar relacionados "
                    f"da meta {meta.codigo}: "
                    f"{error}"
                )

        obras = (
            relacionados.get("obras")
            or []
        )

        projetos = (
            relacionados.get("projetos")
            or []
        )

        metas_relacionadas = (
            relacionados.get("metas")
            or []
        )

        # ====================================================
        # REGIONALIZAÇÃO
        # ====================================================

        regioes: set[str] = set()

        subprefeituras: dict[
            int,
            dict,
        ] = {}

        for obra in obras:

            if not isinstance(
                obra,
                dict,
            ):
                continue

            obra_subprefeituras = (
                obra.get(
                    "subprefeituras"
                )
                or []
            )

            for subprefeitura in (
                obra_subprefeituras
            ):

                if not isinstance(
                    subprefeitura,
                    dict,
                ):
                    continue

                subprefeitura_id = (
                    subprefeitura.get(
                        "id"
                    )
                )

                if isinstance(
                    subprefeitura_id,
                    int,
                ):
                    subprefeituras[
                        subprefeitura_id
                    ] = subprefeitura

                parente_id = (
                    subprefeitura.get(
                        "parente_id"
                    )
                )

                try:
                    parente_id = int(
                        parente_id
                    )

                except (
                    TypeError,
                    ValueError,
                ):
                    continue

                regiao = (
                    REGIOES_POR_PARENTE_ID
                    .get(
                        parente_id
                    )
                )

                if regiao:
                    regioes.add(
                        regiao
                    )

        # ====================================================
        # RETORNO
        # ====================================================

        return {
            "id": meta.id,
            "smae_id": meta.smae_id,

            "codigo": meta.codigo,
            "titulo": meta.titulo,

            "eixo": (
                meta.tema_descricao
                or ""
            ),

            "contexto": (
                meta.contexto
                or ""
            ),

            # Navegação

            "codigo_anterior": (
                codigo_anterior
            ),

            "codigo_proximo": (
                codigo_proximo
            ),

            # Status

            "andamento": (
                classification.andamento
            ),

            "situacao": (
                classification.situacao
            ),

            "prazo": (
                classification.prazo
            ),

            # Classificações

            "orgaos": orgaos,
            "ods": ods,
            "tags": todas_tags,

            # Orçamento

            "orcamento": (
                orcamento_data
            ),

            # Iniciativas

            "iniciativas": (
                iniciativas_data
            ),

            # Regionalização

            "regioes": sorted(
                regioes,
                key=str.casefold,
            ),

            "subprefeituras": sorted(
                subprefeituras.values(),
                key=lambda item: (
                    str(
                        item.get(
                            "descricao",
                            "",
                        )
                    ).casefold()
                ),
            ),

            # Relacionados

            "obras": obras,
            "projetos": projetos,

            "metas_relacionadas": (
                metas_relacionadas
            ),
        }
        
def list_meta_print_options() -> list[dict]:
    """
    Retorna uma listagem leve das metas
    para seleção de impressão.

    Não consulta o SMAE.
    """

    with rx.session() as session:
        rows = session.exec( select( Meta.codigo, Meta.titulo, ) .order_by( Meta.codigo ) ).all()
        return [
            { "codigo": codigo, "titulo": titulo, }
            for codigo, titulo in rows
        ]