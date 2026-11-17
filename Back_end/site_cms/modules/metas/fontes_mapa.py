"""Assoc. rigorosa de dados de metas aos GeoJSON originais, sem alterá-los."""
from __future__ import annotations

from typing import Any
from .fontes_leitor import _key, for_meta, load_geojson, meta_code
from .fontes_wkt import geometry_from_payload

PUBLIC_FLAG = "Localização é públicável?"  # Grafia original, com acento.
# Somente campos conhecidos; dados internos / colunas desconhecidas NAO se publicam.
PUBLIC_GENERAL_FIELDS = {
    "codigo", "Meta", "Eixo", "Indicador", "Descrição Projeto", "Secretaria",
    "Status Regionalização", "Estágio da Ação", "Meta é regionalizável?",
    "Já tem local(is) definido(s)?", PUBLIC_FLAG,
}
PUBLIC_LOCATION_FIELDS = {
    "Subprefeitura", "Distrito", "Endereço", "Latitude", "Longitude",
    "Distrito_Primeira_Ocorrencia",
}
# Relacionamentos inequívocos entre nomes encontrados e camada recebida.
SUB_ALIASES = {
    "casa verde cachoeirinha": "Casa Verde / Limão / Cachoeirinha",
    "casa verde limao cachoeirinha": "Casa Verde / Limão / Cachoeirinha",
    "sao miguel paulista": "São Miguel",
    "perus": "Perus / Anhanguera",
    "perus anhanguera": "Perus / Anhanguera",
}


def _is_public(fields: dict[str, Any]) -> bool:
    return _key(fields.get(PUBLIC_FLAG, "")) == "sim"


def _public_fields(fields: dict[str, Any]) -> dict[str, Any]:
    # Linhas sem permissao espacial podem expor somente campos gerais APOS
    # a liberacao editorial global; nunca endereco, coordenadas ou observacoes.
    allowed = PUBLIC_GENERAL_FIELDS | (PUBLIC_LOCATION_FIELDS if _is_public(fields) else set())
    return {name: value for name, value in fields.items() if name in allowed}


def public_spreadsheet(code: str, *, released: bool) -> dict[str, Any]:
    """API pública: liberada globalmente, com localização apenas onde for Sim.

    Campos editoriais gerais de todas as ações são visíveis após liberação
    global, mas endereço/coordenadas/territórios só com flag Sim.
    A checagem de ficha editorial publicada acontece na FastAPI.
    """
    obj = for_meta(code)
    data = []
    for sheet in obj["abas"]:
        rows = []
        if released:
            for row in sheet["linhas"]:
                rows.append({"linha": row["linha"],
                             "localizacao_publicavel": _is_public(row["campos"]),
                             "campos": _public_fields(row["campos"])})
        data.append({"arquivo": sheet["arquivo"], "aba": sheet["aba"],
                     "total_publicado": len(rows),
                     "com_localizacao_autorizada": sum(1 for r in rows if r["localizacao_publicavel"]),
                     "linhas": rows})
    return {"codigo": obj["codigo"], "fonte_publicada": released,
            "total_abas": len(data), "total_registros_publicos": sum(len(x["linhas"]) for x in data),
            "abas": data}


def match_subprefeituras(value: Any) -> tuple[list[dict], list[str]]:
    features = load_geojson("subprefeituras")["features"]
    index = {_key(f.get("properties", {}).get("nome")): f for f in features}
    found: list[dict] = []
    unknown: list[str] = []
    seen = set()
    for part in str(value or "").split(";"):
        part = part.strip()
        if not part or part in {"-", "."}:
            continue
        match_name = SUB_ALIASES.get(_key(part), part)
        feature = index.get(_key(match_name))
        if not feature:
            unknown.append(part)
            continue
        uid = str(feature.get("properties", {}).get("id"))
        if uid not in seen:
            found.append(feature)
            seen.add(uid)
    return found, unknown


def geojson_meta(code: str, *, public: bool = False) -> dict[str, Any]:
    """Inclui pontos/WKT da tabela e territórios correspondentes, sem chutar pontos."""
    obj = for_meta(code)
    canonical = obj["codigo"]
    features = []
    areas: dict[str, dict] = {}
    unmatched = set()
    without_geometry = 0
    for sheet in obj["abas"]:
        for row in sheet["linhas"]:
            fields = row["campos"]
            if public and not _is_public(fields):
                continue
            if not fields:
                continue
            safe = _public_fields(fields) if public else dict(fields)
            geom, geo_source = geometry_from_payload(fields)
            if geom is not None:
                features.append({"type": "Feature", "geometry": geom,
                                 "properties": {**safe, "codigo_meta": canonical,
                                                "aba_origem": sheet["aba"], "linha_origem": row["linha"],
                                                "tipo_camada": "acao", "fonte_geometria": geo_source}})
            else:
                without_geometry += 1
            linked, missing = match_subprefeituras(fields.get("Subprefeitura", ""))
            unmatched.update(missing)
            for feature in linked:
                uid = str(feature["properties"].get("id"))
                if uid not in areas:
                    areas[uid] = {"type": "Feature", "geometry": feature["geometry"],
                                  "properties": {"codigo_meta": canonical,
                                                 "tipo_camada": "territorio_administrativo",
                                                 "representacao": "subprefeitura_nao_posicao_exata",
                                                 "subprefeitura": feature["properties"].get("nome"),
                                                 "id_subprefeitura": uid}}
    # O arquivo metas.geojson pode estar vazio. Se houver features com id da meta
    # explícito, usar somente aquelas; nunca associar uma geometria sem vínculo.
    linked_file = 0
    for feat in load_geojson("metas")["features"]:
        props = feat.get("properties") or {}
        source_code = next((meta_code(props[k]) for k in ("meta_code", "codigo_meta", "Meta", "meta")
                            if k in props and meta_code(props[k]) is not None), None)
        if source_code != canonical:
            continue
        # Na API pública, as features independentes exigem autorização explicita.
        if public and _key(props.get(PUBLIC_FLAG, props.get("publicavel", ""))) != "sim":
            continue
        linked_file += 1
        features.append(feat if not public else {
            "type": "Feature", "geometry": feat.get("geometry"),
            "properties": {"codigo_meta": canonical, "tipo_camada": "geojson_metas"},
        })
    return {"type": "FeatureCollection", "features": features + list(areas.values()),
            "metadata": {"codigo": canonical, "geometrias": len(features),
                         "poligonos_subprefeituras": len(areas),
                         "geometrias_metas_geojson": linked_file,
                         "sem_geometria": without_geometry,
                         "subprefeituras_nao_identificadas": sorted(unmatched)}}
