"""ALIAS legado da rota 19/11: mantém frontend existente, retorna VERSÃO ATIVA.

A URL tem data por compatibilidade, mas o metadata.data aponta à versão atual.
Prefira /api/site/camadas/metas para novas integrações React.
"""
from typing import Literal
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from Back_end.site_cms.api import camadas_versions_service as service

router = APIRouter(prefix='/api/site/camadas/metas-2026-11-19', tags=['Camadas GEO - URL antiga'])

@router.get('')
def camadas_geral(camada: Literal['linhas', 'poligonos', 'pontos'] | None = None):
    return service.public_collection(camada=camada)

@router.get('/info')
def camadas_info():
    return service.public_info()

@router.get('/gpkg')
def geopackage_original():
    path = service.public_gpkg_path()
    return FileResponse(path, filename=path.name, media_type='application/geopackage+sqlite3')

@router.get('/{codigo}')
def camadas_por_meta(codigo: str, camada: Literal['linhas', 'poligonos', 'pontos'] | None = None):
    n = service.meta_number(codigo)
    if n is None:
        raise HTTPException(status_code=400, detail='Número de meta inválido.')
    return service.public_collection(meta=n, camada=camada)
