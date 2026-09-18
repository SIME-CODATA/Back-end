from collections import defaultdict
from dataclasses import dataclass

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_tag import MetaTag
from Back_end.access_api.metas.models.tag import Tag


ANDAMENTO_TAGS = {
    "Em progresso",
    "Atingida",
    "Em planejamento",
}

SITUACAO_TAGS = {
    "Dentro do cronograma",
    "Risco baixo/médio",
    "Risco alto/muito alto",
    "Meta atingida",
    "Meta comprometida",
}

PRAZO_TAGS = {
    "1º sem/2025",
    "2º sem/2025",
    "1º sem/2026",
    "2º sem/2026",
    "1º sem/2027",
    "2º sem/2027",
    "1º sem/2028",
    "2º sem/2028",
    "Sem previsão",
}


@dataclass(frozen=True)
class MetaClassification:
    """Classificação de negócio de uma Meta."""

    meta_id: int
    codigo: str
    andamento: str
    situacao: str
    prazo: str


def _find_single_tag(
    descriptions: set[str],
    allowed_tags: set[str],
    field_name: str,
    codigo: str,
) -> str:
    """
    Encontra exatamente uma tag de determinada categoria.

    Se houver nenhuma ou mais de uma, considera que os
    dados da Meta estão inconsistentes.
    """

    matches = descriptions & allowed_tags

    if len(matches) != 1:
        raise RuntimeError(
            f"Meta {codigo}: esperado exatamente "
            f"1 valor para '{field_name}', "
            f"mas foram encontrados {len(matches)}: "
            f"{sorted(matches)}"
        )

    return next(iter(matches))


def classify_meta_tags(
    *,
    meta_id: int,
    codigo: str,
    descriptions: set[str],
) -> MetaClassification:
    """
    Transforma as tags de uma Meta nas três
    classificações usadas pelo sistema.
    """

    andamento = _find_single_tag(
        descriptions,
        ANDAMENTO_TAGS,
        "andamento",
        codigo,
    )

    situacao = _find_single_tag(
        descriptions,
        SITUACAO_TAGS,
        "situacao",
        codigo,
    )

    prazo = _find_single_tag(
        descriptions,
        PRAZO_TAGS,
        "prazo",
        codigo,
    )

    return MetaClassification(
        meta_id=meta_id,
        codigo=codigo,
        andamento=andamento,
        situacao=situacao,
        prazo=prazo,
    )


def get_all_meta_classifications() -> list[MetaClassification]:
    """
    Retorna a classificação das metas cadastradas.

    Usa somente PostgreSQL.
    Não consulta o SMAE.
    """

    with rx.session() as session:
        metas = session.exec(
            select(Meta).order_by(Meta.codigo)
        ).all()

        tag_rows = session.exec(
            select(
                MetaTag.meta_id,
                Tag.descricao,
            )
            .join(
                Tag,
                Tag.id == MetaTag.tag_id,
            )
        ).all()

    tags_by_meta: dict[int, set[str]] = defaultdict(set)

    for meta_id, descricao in tag_rows:
        tags_by_meta[meta_id].add(descricao)

    classifications: list[MetaClassification] = []

    for meta in metas:
        if meta.id is None:
            raise RuntimeError(
                f"Meta {meta.codigo} sem ID local."
            )

        classifications.append(
            classify_meta_tags(
                meta_id=meta.id,
                codigo=meta.codigo,
                descriptions=tags_by_meta[meta.id],
            )
        )

    return classifications