from __future__ import annotations

import re
import unicodedata
from copy import deepcopy
from typing import Any

import reflex as rx
from sqlmodel import select

from Back_end.access_api.metas.models.meta import Meta
from Back_end.access_api.metas.models.meta_related_snapshot import (
    MetaRelatedSnapshot,
)
from Back_end.access_api.metas.services.related_snapshot_service import (
    normalize_related_payload,
)
from Back_end.access_api.metas.services.meta_detail_service import (
    get_meta_detail_by_codigo,
)
from Back_end.site_cms.api.meta_schemas import MetaSearchRequest
from Back_end.site_cms.models import CmsMetaContent
from Back_end.site_cms.modules.metas.code import canonical_meta_code


REGIONS_BY_PARENT_ID = {
    181: "Zona Leste",
    182: "Zona Norte",
    183: "Zona Sul",
    184: "Zona Oeste",
    185: "Centro",
}


def _normalized_text(value: Any) -> str:
    raw = str(value or "").strip().casefold()
    decomposed = unicodedata.normalize("NFKD", raw)
    return "".join(
        char
        for char in decomposed
        if not unicodedata.combining(char)
    )


def _sort_code(value: Any) -> tuple[int, int | str]:
    raw = canonical_meta_code(value)
    if raw.isdigit():
        return 0, int(raw)
    return 1, raw.casefold()


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _media_url(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None

    media_id = value.get("media_id")
    if media_id not in (None, ""):
        return f"/api/media/{media_id}/file"

    legacy_source = value.get("legacy_source") or value.get("url")
    if not legacy_source:
        return None

    url = str(legacy_source)
    if url.startswith("http://programademetas.prefeitura.sp.gov.br"):
        url = "https://" + url[len("http://"):]
    return url


def _public_regionalization(value: Any) -> dict[str, Any]:
    data = _as_dict(value)
    blocks = []

    for item in _as_list(data.get("blocks")):
        if not isinstance(item, dict):
            continue
        if not bool(item.get("enabled", True)):
            continue

        blocks.append(
            {
                "chave": str(item.get("key") or ""),
                "titulo": str(item.get("title") or ""),
                "imagem": _media_url(item.get("image")),
                "texto": str(item.get("text") or ""),
                "rodape": str(item.get("footer") or ""),
                "botoes": deepcopy(item.get("buttons") or []),
            }
        )

    return {
        "modo": str(data.get("mode") or "not_regionalizable"),
        "nota": data.get("note"),
        "blocos": blocks,
    }


def _public_actions(value: Any) -> list[dict[str, Any]]:
    result = []
    for item in _as_list(value):
        if not isinstance(item, dict):
            continue
        result.append(
            {
                "numero": str(item.get("number") or ""),
                "descricao": str(item.get("description") or ""),
                "concluida": bool(item.get("completed")),
                "evolucao_destaque": item.get("evolution_label"),
                "evolucao_descricao": item.get("evolution_description"),
            }
        )
    return result


def _public_results(value: Any) -> list[dict[str, Any]]:
    result = []
    for item in _as_list(value):
        if not isinstance(item, dict):
            continue
        result.append(
            {
                "valor": str(item.get("value") or ""),
                "mes": str(item.get("month") or ""),
                "ano": item.get("year"),
                "data": str(item.get("date") or ""),
            }
        )
    return result


def _region_names_from_works(works: list[dict[str, Any]]) -> list[str]:
    result: set[str] = set()

    for work in works:
        for region in work.get("regions") or []:
            text = str(region or "").strip()
            if text:
                result.add(text)

        for subprefecture in work.get("subprefectures") or []:
            if not isinstance(subprefecture, dict):
                continue
            try:
                parent_id = int(subprefecture.get("parent_id"))
            except (TypeError, ValueError):
                continue
            region = REGIONS_BY_PARENT_ID.get(parent_id)
            if region:
                result.add(region)

    return sorted(result, key=str.casefold)


def _subprefecture_names(works: list[dict[str, Any]]) -> list[str]:
    result: set[str] = set()
    for work in works:
        for item in work.get("subprefectures") or []:
            if isinstance(item, dict):
                name = str(item.get("name") or "").strip()
                if name:
                    result.add(name)
    return sorted(result, key=str.casefold)


def _public_work(item: dict[str, Any]) -> dict[str, Any]:
    subprefectures = [
        str(sub.get("name") or "")
        for sub in item.get("subprefectures") or []
        if isinstance(sub, dict) and str(sub.get("name") or "").strip()
    ]
    location = _as_dict(item.get("location"))

    return {
        "id": item.get("id"),
        "codigo": str(item.get("code") or ""),
        "nome": str(item.get("name") or ""),
        "tipo_obra_intervencao": str(item.get("intervention_type") or ""),
        "subprefeituras": subprefectures,
        "subprefeitura": ", ".join(subprefectures),
        "regioes": deepcopy(item.get("regions") or []),
        "equipamento": str(item.get("equipment") or ""),
        "status": str(item.get("status") or ""),
        "percentual_concluido": item.get("percent_complete"),
        "localizacao": {
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "endereco": str(location.get("address") or ""),
        },
    }


def _public_project(item: dict[str, Any]) -> dict[str, Any]:
    location = _as_dict(item.get("location"))
    return {
        "id": item.get("id"),
        "codigo": str(item.get("code") or ""),
        "nome": str(item.get("name") or ""),
        "portfolio": str(item.get("portfolio") or ""),
        "etapa": str(item.get("stage") or ""),
        "localizacao": {
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "endereco": str(location.get("address") or ""),
        },
    }


def _load_rows() -> list[tuple[CmsMetaContent, Meta | None, MetaRelatedSnapshot | None]]:
    with rx.session() as session:
        cms_rows = list(session.exec(select(CmsMetaContent)).all())
        metas = list(session.exec(select(Meta)).all())
        related = list(session.exec(select(MetaRelatedSnapshot)).all())

        metas_by_code = {
            canonical_meta_code(meta.codigo): meta
            for meta in metas
        }
        related_by_meta_id = {
            int(row.meta_id): row
            for row in related
        }

        result = []
        for cms in cms_rows:
            meta = metas_by_code.get(canonical_meta_code(cms.meta_code))
            snapshot = (
                related_by_meta_id.get(int(meta.id))
                if meta is not None and meta.id is not None
                else None
            )
            result.append((cms, meta, snapshot))

        for cms, meta, snapshot in result:
            session.expunge(cms)
            if meta is not None:
                session.expunge(meta)
            if snapshot is not None:
                session.expunge(snapshot)

        return result


def _effective_related(
    content: dict[str, Any],
    snapshot: MetaRelatedSnapshot | None,
) -> dict[str, Any]:
    related = normalize_related_payload(
        snapshot.payload if snapshot is not None else {}
    )

    # Se o editor personalizou obras/projetos, published_content é a fonte
    # oficial. Caso contrário usamos o snapshot persistido do SMAE.
    works = content.get("associated_works")
    if isinstance(works, list) and works:
        related["works"] = deepcopy(works)

    projects = content.get("associated_projects")
    if isinstance(projects, list) and projects:
        related["projects"] = deepcopy(projects)

    return related


def _public_detail_from_row(
    cms: CmsMetaContent,
    meta: Meta | None,
    snapshot: MetaRelatedSnapshot | None,
) -> dict[str, Any] | None:
    content = deepcopy(cms.published_content or {})
    if not content:
        return None

    related = _effective_related(content, snapshot)
    works = related["works"]
    projects = related["projects"]

    title = str(content.get("title") or "")
    title_highlight = str(content.get("title_highlight") or "")
    title_complement = str(content.get("title_complement") or "")

    if not title_complement and title and title_highlight:
        title_complement = title.replace(title_highlight, "", 1).strip(" ,;:-")

    return {
        "codigo": canonical_meta_code(cms.meta_code),
        "numero": str(content.get("number") or cms.meta_code),
        "titulo": title,
        "titulo_destaque": title_highlight,
        "titulo_complemento": title_complement,
        "eixo": {
            "nome": str(content.get("axis_name") or ""),
            "cor_principal": str(content.get("axis_primary_color") or ""),
            "cor_secundaria": str(content.get("axis_secondary_color") or ""),
            "frases": deepcopy(content.get("axis_phrases") or []),
        },
        "projecao": str(content.get("projection") or ""),
        "orgaos_responsaveis": deepcopy(
            content.get("responsible_agencies") or []
        ),
        "acoes_estrategicas": _public_actions(
            content.get("strategic_actions")
        ),
        "monitoramento": {
            "status": str(content.get("monitoring") or ""),
            "resultados_apurados": _public_results(
                content.get("measured_results")
            ),
            "indicador": str(content.get("indicator") or ""),
            "evolucao": str(content.get("evolution") or ""),
        },
        "regionalizacao": _public_regionalization(
            content.get("regionalization")
        ),
        "territorios": {
            "regioes": _region_names_from_works(works),
            "subprefeituras": _subprefecture_names(works),
        },
        "obras_associadas": [
            _public_work(item)
            for item in works
            if isinstance(item, dict)
        ],
        "projetos_associados": [
            _public_project(item)
            for item in projects
            if isinstance(item, dict)
        ],
        "metas_relacionadas": deepcopy(related["related_metas"]),
        "secoes_extras": deepcopy(content.get("extra_sections") or []),
        "smae": {
            "id": meta.smae_id if meta is not None else cms.smae_meta_id,
            "sincronizado_em": (
                snapshot.synced_at.isoformat()
                if snapshot is not None and snapshot.synced_at is not None
                else None
            ),
        },
    }


def _smae_code_from_public_code(value: Any) -> str:
    """Converte o código público/CMS (01, 56, 132) para o código SMAE."""
    raw = str(value or "").strip()
    if raw.isdigit():
        return raw.zfill(3)
    return raw


def _merge_operational_detail(
    public_detail: dict[str, Any],
    operational: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Enriquece a ficha pública com dados vivos já normalizados do SMAE.

    O conteúdo editorial do CMS continua separado e nunca é sobrescrito
    por campos apenas parecidos do SMAE.
    """
    if not operational:
        public_detail["dados_smae_disponiveis"] = False
        return public_detail

    orgaos = []
    for item in operational.get("orgaos") or []:
        if not isinstance(item, dict):
            continue
        orgaos.append({
            "sigla": str(item.get("sigla") or ""),
            "descricao": str(item.get("descricao") or ""),
            "responsavel": bool(item.get("responsavel")),
        })

    subprefeituras = []
    for item in operational.get("subprefeituras") or []:
        if not isinstance(item, dict):
            continue
        subprefeituras.append({
            "id": item.get("id"),
            "descricao": str(item.get("descricao") or ""),
            "nivel": item.get("nivel"),
            "parente_id": item.get("parente_id"),
        })

    public_detail.update({
        "dados_smae_disponiveis": True,
        "contexto": str(operational.get("contexto") or ""),
        "navegacao": {
            "anterior": canonical_meta_code(operational.get("codigo_anterior")),
            "proxima": canonical_meta_code(operational.get("codigo_proximo")),
        },
        "status_smae": {
            "andamento": str(operational.get("andamento") or ""),
            "situacao": str(operational.get("situacao") or ""),
            "previsao": str(operational.get("prazo") or ""),
        },
        "classificacoes": {
            "orgaos": orgaos,
            "ods": list(operational.get("ods") or []),
            "tags": list(operational.get("tags") or []),
        },
        "orcamento": deepcopy(operational.get("orcamento")),
        "iniciativas": deepcopy(operational.get("iniciativas") or []),
        "territorios_smae": {
            "regioes": list(operational.get("regioes") or []),
            "subprefeituras": subprefeituras,
        },
    })

    # Obras/projetos públicos já vêm do snapshot persistido e normalizado.
    # O domínio operacional é mantido apenas como fonte complementar.
    return public_detail


def get_public_meta_detail(code: str) -> dict[str, Any] | None:
    normalized = canonical_meta_code(code)
    for cms, meta, snapshot in _load_rows():
        if canonical_meta_code(cms.meta_code) != normalized:
            continue

        detail = _public_detail_from_row(cms, meta, snapshot)
        if detail is None:
            return None

        smae_code = (
            str(meta.codigo)
            if meta is not None and str(meta.codigo or "").strip()
            else _smae_code_from_public_code(normalized)
        )

        operational = None
        try:
            operational = get_meta_detail_by_codigo(smae_code)
        except Exception as error:
            # A ficha editorial continua disponível mesmo se houver falha
            # inesperada na camada operacional.
            print(
                "Erro ao enriquecer ficha pública da meta "
                f"{normalized} com dados SMAE locais: {error}"
            )

        return _merge_operational_detail(detail, operational)

    return None


def list_public_meta_cards() -> list[dict[str, Any]]:
    result = []
    for cms, meta, snapshot in _load_rows():
        detail = _public_detail_from_row(cms, meta, snapshot)
        if detail is None:
            continue

        result.append(
            {
                "codigo": detail["codigo"],
                "numero": detail["numero"],
                "titulo": detail["titulo"],
                "titulo_destaque": detail["titulo_destaque"],
                "titulo_complemento": detail["titulo_complemento"],
                "eixo": detail["eixo"],
                "monitoramento": detail["monitoramento"]["status"],
                "regioes": detail["territorios"]["regioes"],
                "subprefeituras": detail["territorios"]["subprefeituras"],
                "tem_obras": bool(detail["obras_associadas"]),
                "regionalizada": (
                    detail["regionalizacao"]["modo"]
                    != "not_regionalizable"
                ),
            }
        )

    return sorted(result, key=lambda item: _sort_code(item["codigo"]))


def _contains_any(value: Any, needles: list[str]) -> bool:
    haystack = _normalized_text(value)
    return any(_normalized_text(needle) in haystack for needle in needles)


def _matches_search(detail: dict[str, Any], filters: MetaSearchRequest) -> bool:
    if filters.texto.strip():
        searchable = [
            detail.get("codigo"),
            detail.get("titulo"),
            detail.get("projecao"),
            detail.get("monitoramento", {}).get("indicador"),
            detail.get("monitoramento", {}).get("evolucao"),
            " ".join(detail.get("orgaos_responsaveis") or []),
            " ".join(
                str(item.get("descricao") or "")
                for item in detail.get("acoes_estrategicas") or []
            ),
            " ".join(
                str(item.get("nome") or "")
                for item in detail.get("obras_associadas") or []
            ),
        ]
        term = _normalized_text(filters.texto)
        if term not in _normalized_text(" ".join(str(x or "") for x in searchable)):
            return False

    if filters.eixos and not _contains_any(
        detail.get("eixo", {}).get("nome"), filters.eixos
    ):
        return False

    if filters.orgaos:
        agencies = detail.get("orgaos_responsaveis") or []
        if not any(
            _normalized_text(wanted) == _normalized_text(agency)
            for wanted in filters.orgaos
            for agency in agencies
        ):
            return False

    if filters.monitoramento:
        status = _normalized_text(
            detail.get("monitoramento", {}).get("status")
        )
        if status not in {
            _normalized_text(value)
            for value in filters.monitoramento
        }:
            return False

    territories = detail.get("territorios") or {}
    if filters.subprefeituras:
        current = {_normalized_text(x) for x in territories.get("subprefeituras") or []}
        if not current.intersection({_normalized_text(x) for x in filters.subprefeituras}):
            return False

    if filters.regioes:
        current = {_normalized_text(x) for x in territories.get("regioes") or []}
        if not current.intersection({_normalized_text(x) for x in filters.regioes}):
            return False

    works = detail.get("obras_associadas") or []
    if filters.com_obras is not None and bool(works) != filters.com_obras:
        return False

    if filters.tipos_obra:
        current = {
            _normalized_text(item.get("tipo_obra_intervencao"))
            for item in works
        }
        if not current.intersection({_normalized_text(x) for x in filters.tipos_obra}):
            return False

    if filters.equipamentos:
        current = {
            _normalized_text(item.get("equipamento"))
            for item in works
        }
        if not current.intersection({_normalized_text(x) for x in filters.equipamentos}):
            return False

    if filters.regionalizada is not None:
        is_regionalized = (
            detail.get("regionalizacao", {}).get("modo")
            != "not_regionalizable"
        )
        if is_regionalized != filters.regionalizada:
            return False

    return True


def search_public_metas(filters: MetaSearchRequest) -> dict[str, Any]:
    details: list[dict[str, Any]] = []

    for cms, meta, snapshot in _load_rows():
        detail = _public_detail_from_row(cms, meta, snapshot)
        if detail is not None and _matches_search(detail, filters):
            details.append(detail)

    details.sort(key=lambda item: _sort_code(item["codigo"]))
    total = len(details)
    page = details[filters.offset:filters.offset + filters.limit]

    return {
        "total": total,
        "offset": filters.offset,
        "limit": filters.limit,
        "metas": [
            {
                "codigo": item["codigo"],
                "numero": item["numero"],
                "titulo": item["titulo"],
                "titulo_destaque": item["titulo_destaque"],
                "titulo_complemento": item["titulo_complemento"],
                "eixo": item["eixo"],
                "monitoramento": item["monitoramento"]["status"],
                "regioes": item["territorios"]["regioes"],
                "subprefeituras": item["territorios"]["subprefeituras"],
                "tem_obras": bool(item["obras_associadas"]),
                "regionalizada": (
                    item["regionalizacao"]["modo"]
                    != "not_regionalizable"
                ),
            }
            for item in page
        ],
    }


def get_public_filter_options() -> dict[str, list[str]]:
    eixos: set[str] = set()
    orgaos: set[str] = set()
    monitoramento: set[str] = set()
    subprefeituras: set[str] = set()
    regioes: set[str] = set()
    tipos_obra: set[str] = set()
    equipamentos: set[str] = set()

    for cms, meta, snapshot in _load_rows():
        detail = _public_detail_from_row(cms, meta, snapshot)
        if detail is None:
            continue

        axis = str(detail["eixo"].get("nome") or "").strip()
        if axis:
            eixos.add(axis)

        orgaos.update(str(x).strip() for x in detail["orgaos_responsaveis"] if str(x).strip())
        status = str(detail["monitoramento"].get("status") or "").strip()
        if status:
            monitoramento.add(status)

        subprefeituras.update(detail["territorios"]["subprefeituras"])
        regioes.update(detail["territorios"]["regioes"])

        for work in detail["obras_associadas"]:
            kind = str(work.get("tipo_obra_intervencao") or "").strip()
            equipment = str(work.get("equipamento") or "").strip()
            if kind:
                tipos_obra.add(kind)
            if equipment:
                equipamentos.add(equipment)

    sort = lambda values: sorted(values, key=str.casefold)
    return {
        "eixos": sort(eixos),
        "orgaos": sort(orgaos),
        "monitoramento": sort(monitoramento),
        "subprefeituras": sort(subprefeituras),
        "regioes": sort(regioes),
        "tipos_obra": sort(tipos_obra),
        "equipamentos": sort(equipamentos),
    }


def _geometry_from_location(location: dict[str, Any]) -> dict[str, Any] | None:
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    if latitude is None or longitude is None:
        return None
    try:
        return {
            "type": "Point",
            "coordinates": [float(longitude), float(latitude)],
        }
    except (TypeError, ValueError):
        return None


def _geo_feature_from_public_work(
    *,
    meta_code: str,
    work: dict[str, Any],
) -> dict[str, Any]:
    location = work.get("localizacao") or {}
    return {
        "type": "Feature",
        "geometry": _geometry_from_location(location),
        "properties": {
            "meta_code": meta_code,
            "source_type": "work",
            "id": work.get("id"),
            "code": work.get("codigo"),
            "name": work.get("nome"),
            "status": work.get("status"),
            "percent_complete": work.get("percentual_concluido"),
            "address": location.get("endereco") or "",
            "subprefectures": work.get("subprefeituras") or [],
            "regions": work.get("regioes") or [],
            "intervention_type": work.get("tipo_obra_intervencao") or "",
            "equipment": work.get("equipamento") or "",
        },
    }


def _geo_feature_from_public_project(
    *,
    meta_code: str,
    project: dict[str, Any],
) -> dict[str, Any]:
    location = project.get("localizacao") or {}
    return {
        "type": "Feature",
        "geometry": _geometry_from_location(location),
        "properties": {
            "meta_code": meta_code,
            "source_type": "project",
            "id": project.get("id"),
            "code": project.get("codigo"),
            "name": project.get("nome"),
            "portfolio": project.get("portfolio") or "",
            "stage": project.get("etapa") or "",
            "address": location.get("endereco") or "",
        },
    }


def _map_features_from_detail(detail: dict[str, Any]) -> list[dict[str, Any]]:
    features = [
        _geo_feature_from_public_work(
            meta_code=detail["codigo"],
            work=work,
        )
        for work in detail.get("obras_associadas") or []
    ]
    features.extend(
        _geo_feature_from_public_project(
            meta_code=detail["codigo"],
            project=project,
        )
        for project in detail.get("projetos_associados") or []
    )
    return features


def get_public_meta_map(code: str) -> dict[str, Any] | None:
    detail = get_public_meta_detail(code)
    if detail is None:
        return None
    return {
        "type": "FeatureCollection",
        "meta_codigo": detail["codigo"],
        "features": _map_features_from_detail(detail),
    }


def get_public_map() -> dict[str, Any]:
    features: list[dict[str, Any]] = []
    for cms, meta, snapshot in _load_rows():
        detail = _public_detail_from_row(cms, meta, snapshot)
        if detail is not None:
            features.extend(_map_features_from_detail(detail))
    return {
        "type": "FeatureCollection",
        "features": features,
    }
