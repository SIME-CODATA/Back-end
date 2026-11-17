"""Rotas aditivas FastAPI, independentes de cms_meta_geo_records.

Para publicar linhas do arquivo é preciso habilitar CMS_METAS_PUBLICAR_FONTES=1,
exigir ficha editorial publicada e verificar sinalizacao Sim na origem.
"""
from __future__ import annotations

import os
from typing import Literal
from fastapi import APIRouter, HTTPException, Cookie, Query

from Back_end.site_cms.api.public_service import get_public_meta
from Back_end.access.modules.auth.service import validate_session
from Back_end.access.modules.users.service import get_user_by_id
from Back_end.access.core.guards import can_access
from Back_end.access.core.permissions import Permission
from .fontes_leitor import load_geojson, meta_code, for_meta, all_sheets
from .fontes_mapa import geojson_meta, public_spreadsheet

fontes_router = APIRouter(tags=["Fontes das Metas"])



# PUBLICACAO_SEGURA_METAS_V1
# Esta política publica SOMENTE linhas da aba de monitores marcadas com "Sim".
# "Não", "Parcialmente" e campos sem autorização não são publicados.
# Outras abas permanecem completas apenas na visão administrativa autenticada.
from collections import Counter
import math
from .fontes_leitor import for_meta, _key
from .fontes_mapa import match_subprefeituras
from .fontes_wkt import point_from_values, parse_wkt, valid_sp_geometry

_ABA_PRINCIPAL = "02_GESTAO_MONITORES"
_PUBLIC_FIELDS = (
    "codigo", "Meta", "Eixo", "Indicador", "Descrição Projeto", "Secretaria",
    "Status Regionalização", "Estágio da Ação", "Meta é regionalizável?",
    "Já tem local(is) definido(s)?", "Localização é públicável?",
    "Subprefeitura", "Distrito", "Endereço",
)
# Nunca publicar Observações adicionais, formulas, células originais, buffer,
# notas internas, GEO/QGIS independente, nem o texto integral do Excel.


def _publicacao_automatica_autorizada(code: str) -> bool:
    """Piloto explícito por código. Nunca publica tudo por padrão."""
    raw = os.getenv("CMS_METAS_PUBLICACAO_SEGURA", "").strip()
    if not raw:
        return False
    if _key(raw) in {"todas", "all"}:
        return True
    permitidos = {meta_code(x.strip()) for x in raw.split(",")}
    return code in permitidos


def _campos_aprovados(code: str):
    """Reaproveita a aba principal, preservando vínculos e origem."""
    obj = for_meta(code)
    principal = next((s for s in obj["abas"] if s["aba"] == _ABA_PRINCIPAL), None)
    if principal is None:
        return [], obj
    itens = [r for r in principal["linhas"] if r.get("tipo") == "dado"]
    contagem_codigos = Counter(str(r.get("campos", {}).get("codigo") or "").strip()
                               for r in itens)
    aprovados = []
    for r in itens:
        f = r.get("campos") or {}
        cod_acao = str(f.get("codigo") or "").strip()
        # Não publicar ações ambíguas, sem código ou com divulgação parcial.
        if not cod_acao or contagem_codigos[cod_acao] != 1:
            continue
        if _key(f.get("Localização é públicável?")) != "sim":
            continue
        status = _key(f.get("Status Regionalização"))
        if "sem publicidade" in status or "devido a publicidade" in status:
            continue
        aprovados.append(r)
    return aprovados, obj


def _km_aprox(a: list[float], b: list[float]) -> float:
    return math.hypot((a[1] - b[1]) * 111.0,
                      (a[0] - b[0]) * 102.0)


def _coordenada_validada(fields: dict, derivados: dict) -> dict | None:
    """Não publicar ponto quando há divergência >250 m com GEO_PDM.

    Nunca usa a geometria derivada para corrigir o ponto original. O valor
    discrepante permanece íntegro no modo administrativo, para revisão.
    """
    ponto = point_from_values(fields.get("Latitude"), fields.get("Longitude"))
    if not ponto:
        return None
    if not derivados:
        return ponto
    if _key(derivados.get("Validacao_Espacial")) not in {"", "ok"}:
        return None
    base = ponto["coordinates"]
    geo = point_from_values(derivados.get("Latitude_WGS"), derivados.get("Longitude_WGS"))
    if geo and _km_aprox(base, geo["coordinates"]) > .25:
        return None
    wkt = str(derivados.get("Geometria_WKT") or "").strip()
    if wkt:
        try:
            geom = parse_wkt(wkt)
        except ValueError:
            return None
        if geom["type"] == "Point" and (
            not valid_sp_geometry(geom) or _km_aprox(base, geom["coordinates"]) > .25
        ):
            return None
    return ponto


def _dados_publicos_controlados(code: str) -> tuple[dict, dict]:
    """Uma fonte de verdade para /fontes, /fontes/geojson e /completa."""
    aprovados, obj = _campos_aprovados(code)
    derivados = {}
    for sheet in obj["abas"]:
        if sheet["aba"] == "03_GEO_PDM":
            for r in sheet["linhas"]:
                f = r.get("campos", {})
                cod = str(f.get("Geocodigo") or "").strip()
                if cod:
                    # Se houver códigos GEO duplicados, a posição não é confiável.
                    derivados.setdefault(cod, []).append(f)

    registros = []
    features = []
    territorios = {}
    rejeitadas_geometria = 0
    for r in aprovados:
        orig = r["campos"]
        codigo_acao = str(orig["codigo"]).strip()
        safe = {k: orig[k] for k in _PUBLIC_FIELDS if k in orig and orig[k] not in (None, "")}
        candidatos = derivados.get(codigo_acao, [])
        ponto = _coordenada_validada(orig, candidatos[0] if len(candidatos) == 1 else {})
        if len(candidatos) > 1:
            ponto = None
        if not ponto and (orig.get("Latitude") or orig.get("Longitude")):
            rejeitadas_geometria += 1
        if ponto:
            safe["Latitude"] = ponto["coordinates"][1]
            safe["Longitude"] = ponto["coordinates"][0]
        else:
            # Endereço exato fica retido quando a geografia está divergente.
            safe.pop("Endereço", None)
        registros.append({"linha": r["linha"], "localizacao_publicavel": bool(ponto),
                          "campos": safe})
        if ponto:
            features.append({
                "type": "Feature", "geometry": ponto,
                "properties": {**safe, "codigo_meta": code, "tipo_camada": "acao",
                               "fonte": _ABA_PRINCIPAL},
            })
        # Polígono administrativo nunca é apresentado como a posição da ação.
        nomes = orig.get("Subprefeitura", "")
        matches, _ = match_subprefeituras(nomes)
        for sp in matches:
            props = sp.get("properties", {})
            uid = str(props.get("id"))
            territorios[uid] = {
                "type": "Feature", "geometry": sp["geometry"],
                "properties": {"codigo_meta": code, "tipo_camada": "territorio_administrativo",
                               "representacao": "area_administrativa_nao_ponto_exato",
                               "subprefeitura": props.get("nome"), "id_subprefeitura": uid},
            }
    abas = []
    for sh in obj["abas"]:
        linhas = registros if sh["aba"] == _ABA_PRINCIPAL else []
        abas.append({"arquivo": sh["arquivo"], "aba": sh["aba"],
                     "total_publicado": len(linhas),
                     "com_localizacao_autorizada": sum(bool(x["localizacao_publicavel"]) for x in linhas),
                     "linhas": linhas})
    fontes = {"codigo": code, "fonte_publicada": True, "total_abas": len(abas),
              "total_registros_publicos": len(registros), "abas": abas}
    mapa = {"type": "FeatureCollection", "features": features + list(territorios.values()),
            "metadata": {"codigo": code, "fonte_publicada": True,
                         "geometrias": len(features),
                         "poligonos_subprefeituras": len(territorios),
                         "localizacoes_pendentes_revisao": rejeitadas_geometria,
                         "regra": "Somente 02_GESTAO_MONITORES com autorização Sim; sem notas internas"}}
    return fontes, mapa


def _fontes_e_mapa(code: str) -> tuple[dict, dict, bool]:
    if _publicacao_automatica_autorizada(code):
        fontes, mapa = _dados_publicos_controlados(code)
        return fontes, mapa, True
    return public_spreadsheet(code, released=False), {
        "type": "FeatureCollection", "features": [],
        "metadata": {"codigo": code, "fonte_publicada": False},
    }, False


def _public_meta(code: str) -> str:
    canonical = meta_code(code)
    if canonical is None:
        raise HTTPException(status_code=400, detail="Codigo da Meta invalido")
    if get_public_meta(canonical) is None:
        raise HTTPException(status_code=404, detail="Meta nao publicada")
    return canonical


def _released() -> bool:
    return os.getenv("CMS_METAS_PUBLICAR_FONTES", "0").strip() == "1"


@fontes_router.get("/metas/{codigo}/fontes")
def fonte_planilha_por_meta(codigo: str):
    code = _public_meta(codigo)
    fontes, _, _ = _fontes_e_mapa(code)
    return fontes



@fontes_router.get("/metas/{codigo}/fontes/geojson")
def fonte_mapa_por_meta(codigo: str):
    code = _public_meta(codigo)
    _, mapa, _ = _fontes_e_mapa(code)
    return mapa



@fontes_router.get("/fontes/camadas/{nome}")
def fonte_camada(nome: str):
    if nome not in {"subprefeituras", "mascara"}:
        raise HTTPException(status_code=404, detail="Camada nao encontrada")
    try:
        return load_geojson(nome)
    except (OSError, ValueError) as error:
        raise HTTPException(status_code=503, detail="Camada indisponivel") from error


def _require_admin_session(token: str | None) -> None:
    """Autoriza a visualizacao de linhas internas, sem publicar suas localizacoes."""
    user_id = validate_session(token or "")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Sessao administrativa obrigatoria")
    user = get_user_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario inativo ou inexistente")
    if not can_access(user.role, Permission.SITE_VIEW):
        raise HTTPException(status_code=403, detail="Sem permissao para consultar fontes internas")


@fontes_router.get("/metas/{codigo}/completa")
def meta_com_fontes_e_mapa(
    codigo: str,
    visao: Literal["publica", "administrativa"] = Query(
        "publica", description="Visao publica ou dados originais para usuario autorizado"
    ),
    incluir_camadas: bool = Query(
        False, description="Inclui os GeoJSON completos das camadas compartilhadas"
    ),
    pdm_session: str | None = Cookie(default=None, alias="pdm_session"),
):
    """Ficha publicada, 13 abas identificadas e mapa, sem expor dados internos."""
    code = _public_meta(codigo)
    administrative = visao == "administrativa"
    if administrative:
        _require_admin_session(pdm_session)

    fontes_publicas, mapa_publico, released = _fontes_e_mapa(code)
    abas_excel = {}
    if administrative:
        conjunto = for_meta(code)
        originais = {sheet["aba"]: sheet for sheet in all_sheets()}
        for sheet in conjunto["abas"]:
            nome = sheet["aba"]
            referencia = sheet["tipo"] == "referencia_global"
            linhas = originais[nome]["linhas"] if referencia else sheet["linhas"]
            registros = [{
                "linha_excel": linha["linha"],
                "tipo_linha": linha["tipo"],
                "campos": linha.get("campos", {}),
                "celulas_originais": linha["celulas"],
                "formulas": linha.get("formulas", {}),
                "vinculo": linha.get("vinculo"),
            } for linha in linhas]
            abas_excel[nome] = {"tipo": sheet["tipo"], "arquivo": sheet["arquivo"],
                                "total_registros": len(registros), "registros": registros}
    else:
        for sheet in fontes_publicas["abas"]:
            abas_excel[sheet["aba"]] = {
                "tipo": "publicada_filtrada", "arquivo": sheet["arquivo"],
                "total_registros": sheet["total_publicado"], "registros": sheet["linhas"],
            }

    camadas_geojson = {"mapa_meta": (
        geojson_meta(code, public=False) if administrative else mapa_publico
    )}
    for camada in ("subprefeituras", "mascara"):
        camadas_geojson[camada] = (
            load_geojson(camada) if incluir_camadas else {
                "endpoint": f"/api/site/fontes/camadas/{camada}", "escopo": "compartilhado"
            }
        )
    # Nunca entregar o arquivo bruto caso passe a conter geometrias restritas.
    camadas_geojson["metas_geojson"] = (
        load_geojson("metas") if administrative
        else {"type": "FeatureCollection", "features": []}
    )
    return {
        "codigo": code,
        "meta": get_public_meta(code),
        "fontes": fontes_publicas,
        "mapa": mapa_publico,
        "abas_excel": abas_excel,
        "camadas_geojson": camadas_geojson,
        "resumo": {
            "visao": visao,
            "total_abas": len(abas_excel),
            "registros_retornados": sum(x["total_registros"] for x in abas_excel.values()),
            "fontes_publicadas": released,
            "camadas_embutidas": incluir_camadas,
        },
    }

