"""Testes do gerenciador; não escrevem em ambiente real nem publicam nada real."""
import json
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from Back_end.site_cms.api import camadas_versions_service as service
from Back_end.site_cms.api.camadas_ativas_router import router as active_router
from Back_end.site_cms.api.camadas_2026_11_19 import router as old_router


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setenv('CMS_CAMADAS_STORAGE_PATH', str(tmp_path / 'geo_store'))
    return tmp_path


def test_original_e_alias(setup):
    app = FastAPI()
    app.include_router(active_router)
    app.include_router(old_router)
    client = TestClient(app)
    for url in ['/api/site/camadas/metas', '/api/site/camadas/metas-2026-11-19']:
        response = client.get(url)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data['features']) == 25
        assert data['metadata']['versao_ativa'] == service.BASE_ID
        assert len(client.get(url + '/53').json()['features']) == 4
        assert len(client.get(url + '/54').json()['features']) == 2
        assert len(client.get(url + '?camada=linhas').json()['features']) == 21
        assert len(client.get(url + '?camada=poligonos').json()['features']) == 4
        assert client.get(url + '/gpkg').status_code == 403


def test_upload_rascunho_e_ativacao_e_retorno(setup):
    raw = service.BASE_JSON.read_bytes()
    original_count = len(service.public_collection()['features'])
    draft = service.create_draft(geojson_bytes=raw, gpkg_bytes=service.BASE_GPKG.read_bytes(),
                                 data_referencia='2026-11-25', descricao='Atualização 1',actor_id=7)
    assert service.active_id() == service.BASE_ID  # upload NÃO publica
    assert len(service.list_versions()) == 2
    assert (service.storage_dir() / 'versions' / draft['id'] / 'original.gpkg').exists()
    service.publish(draft['id'],actor_id=7)
    assert service.active_id() == draft['id']
    assert len(service.public_collection()['features']) == original_count
    service.publish(service.BASE_ID,actor_id=7)
    assert service.active_id() == service.BASE_ID


def test_arquivo_incompleto_nao_substitui_ativo(setup):
    raw = json.loads(service.BASE_JSON.read_text(encoding='utf8'))
    raw['features'] = raw['features'][:-1]
    draft = service.create_draft(geojson_bytes=json.dumps(raw).encode(), gpkg_bytes=None,
                                 data_referencia='2026-11-26', descricao='Perdendo linha',actor_id=7)
    with pytest.raises(ValueError, match='não contém'):
        service.publish(draft['id'],actor_id=7)
    assert service.active_id() == service.BASE_ID
    service.publish(draft['id'],actor_id=7,allow_missing=True)
    assert len(service.public_collection()['features']) == 24
    assert len(service.list_versions()) == 2


def test_nao_expõe_internos_e_recusa_invalido(setup):
    response = service.public_collection(meta=53)
    assert len(response['features']) == 4
    assert all('WKT' not in f['properties'] for f in response['features'])
    with pytest.raises(ValueError):
        service.create_draft(geojson_bytes=b'{}',gpkg_bytes=None,
                              data_referencia='2026-11-25',descricao='',actor_id=7)
    assert service.active_id() == service.BASE_ID


def test_atualizacao_com_mais_geometrias(setup):
    data = json.loads(service.BASE_JSON.read_text(encoding='utf8'))
    extra = json.loads(json.dumps(data['features'][-1]))
    extra['properties']['Código'] = '54.99.01'
    extra['properties']['Trecho'] = 'Novo trecho validado'
    data['features'].append(extra)
    draft = service.create_draft(
        geojson_bytes=json.dumps(data).encode('utf8'), gpkg_bytes=None,
        data_referencia='2026-11-27', descricao='Novo trecho', actor_id=7)
    assert service.active_id() == service.BASE_ID
    service.publish(draft['id'], actor_id=7)
    assert len(service.public_collection()['features']) == 26
    assert service.public_collection()['metadata']['data'] == '2026-11-27'
    assert len(service.public_collection(meta=54)['features']) == 3


def test_gpkg_inconsistente_rejeitado_antes_de_arquivar(setup):
    data = json.loads(service.BASE_JSON.read_text(encoding='utf8'))
    data['features'] = data['features'][:-1]
    with pytest.raises(ValueError, match='divergem'):
        service.create_draft(
            geojson_bytes=json.dumps(data).encode('utf8'),
            gpkg_bytes=service.BASE_GPKG.read_bytes(),
            data_referencia='2026-11-28', descricao='GPKG antigo', actor_id=7)
    assert len(service.list_versions()) == 1
    assert service.active_id() == service.BASE_ID
