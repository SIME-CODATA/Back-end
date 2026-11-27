"""Rotas públicas estáveis da fonte de camadas GEO independente do Excel."""
from typing import Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from Back_end.site_cms.api import camadas_versions_service as service

router = APIRouter(prefix='/api/site/camadas/metas', tags=['Site CMS - Camadas GEO (atual)'])


@router.get('', summary='GeoJSON da versão GEO publicada atualmente')
def geral(camada: Literal['linhas', 'poligonos', 'pontos'] | None = None):
    return service.public_collection(camada=camada)


@router.get('/info', summary='Versão ativa e totais da fonte GEO')
def info():
    return service.public_info()


@router.get('/gpkg', summary='Download GeoPackage da versão ativa, sujeito a autorização')
def gpkg():
    path = service.public_gpkg_path()
    return FileResponse(path, filename=path.name, media_type='application/geopackage+sqlite3')


@router.get('/{codigo}', summary='GeoJSON da versão ativa filtrado por meta')
def por_meta(codigo: str, camada: Literal['linhas', 'poligonos', 'pontos'] | None = None):
    n = service.meta_number(codigo)
    if n is None:
        raise HTTPException(status_code=400, detail='Número da meta inválido.')
    return service.public_collection(meta=n, camada=camada)
