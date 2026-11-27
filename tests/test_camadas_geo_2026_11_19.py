"""Teste isolado do router. Rodar: uv run python -m pytest tests/test_camadas_geo_2026_11_19.py
Se pytest não estiver instalado: uv run --with pytest python -m pytest tests/test_camadas_geo_2026_11_19.py
"""
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient

from Back_end.site_cms.api.camadas_2026_11_19 import router

client_app = FastAPI()
client_app.include_router(router)
client = TestClient(client_app)
BASE = "/api/site/camadas/metas-2026-11-19"


def test_geral():
    r = client.get(BASE)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 25
    assert all(feat["properties"]["Localização é públicável?"] == "Sim" for feat in data["features"])
    assert all("WKT" not in feat["properties"] for feat in data["features"])


def test_camadas():
    assert len(client.get(BASE, params={"camada": "linhas"}).json()["features"]) == 21
    assert len(client.get(BASE, params={"camada": "poligonos"}).json()["features"]) == 4


def test_metas_e_identificadores():
    assert len(client.get(BASE + "/53").json()["features"]) == 4
    m54 = client.get(BASE + "/54").json()["features"]
    assert len(m54) == 2
    assert {f["properties"]["Trecho"] for f in m54} == {"Linha 1 (vermelha)", "Linha 2 (azul)"}
    assert client.get(BASE + "/01").json()["features"] == []
    assert client.get(BASE + "/53.01.01").status_code == 400


def test_info_e_gpkg_privado_por_padrao(monkeypatch):
    monkeypatch.delenv("CMS_CAMADAS_GPKG_DOWNLOAD_PUBLICO", raising=False)
    assert client.get(BASE + "/info").json()["total_publicavel"] == 25
    assert client.get(BASE + "/gpkg").status_code == 403
