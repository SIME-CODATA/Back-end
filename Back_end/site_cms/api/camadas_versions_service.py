"""Armazenamento versionado de camadas GEO, INDEPENDENTE do Excel e PostgreSQL.

O arquivo original de 19/11/2026 é a versão base. Uploads ficam em diretórios
imutáveis num volume persistente; publicação altera somente o ponteiro active.json.
Não contém endpoints de escrita públicos; a escrita é chamada por eventos Reflex
autenticados que verificam SITE_EDIT / SITE_PUBLISH.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import sqlite3
import threading
import uuid
from collections import Counter
from datetime import date, datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import HTTPException

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
BASE_FOLDER = HERE.parent / 'modules' / 'metas' / 'data' / 'camadas_geograficas' / '2026_11_19'
BASE_JSON = BASE_FOLDER / 'metas_pdm_2026_11_19.geojson'
BASE_GPKG = BASE_FOLDER / 'metas_pdm_2026_11_19.gpkg'
BASE_ID = '2026-11-19-base'
MAX_JSON_BYTES = 30 * 1024 * 1024
MAX_GPKG_BYTES = 120 * 1024 * 1024
PUBLIC_FLAG = 'Localização é públicável?'
PUBLIC_FIELDS = (
    'Código', 'Meta', 'Eixo', 'Tipo', 'Ação Estratégica', 'Descrição da Meta',
    'Descrição Projeto', 'Trecho', 'Secretaria', 'Subprefeitura', 'Distrito',
    'Endereço', 'Latitude_WGS', 'Longitude_WGS', 'Meta é regionalizável?',
    'Já tem local(is) definido(s)?', PUBLIC_FLAG, 'Status Regionalização',
    'Status Execução', 'Tipo de Mapa', 'Tipo de Dado', 'Informações complementares',
    'Extensão (km)', 'Área (ha)',
)
ALLOWED_LAYERS = {'linhas', 'poligonos', 'pontos'}
GEOM_LAYERS = {
    'LineString': 'linhas', 'MultiLineString': 'linhas',
    'Polygon': 'poligonos', 'MultiPolygon': 'poligonos',
    'Point': 'pontos', 'MultiPoint': 'pontos',
}
_LOCK = threading.RLock()
_ID_RE = re.compile(r'^\d{4}-\d{2}-\d{2}-(?:[0-9a-f]{12}|base)$')


def storage_dir() -> Path:
    return Path(os.environ.get('CMS_CAMADAS_STORAGE_PATH', str(REPO_ROOT / 'data' / 'camadas_geo'))).resolve()


def _versions_dir() -> Path:
    return storage_dir() / 'versions'


def _version_dir(version_id: str) -> Path:
    if not _ID_RE.fullmatch(version_id):
        raise ValueError('Identificador de versão inválido.')
    return _versions_dir() / version_id


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def _write_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name('.' + path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with tmp.open('w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def _read_json(path: Path) -> dict:
    with path.open('r', encoding='utf-8') as f:
        result = json.load(f)
    if not isinstance(result, dict):
        raise ValueError('JSON principal não é um objeto.')
    return result


def _pairs(node: Any):
    if isinstance(node, list):
        if len(node) >= 2 and all(isinstance(v, (float, int)) and not isinstance(v, bool) for v in node[:2]):
            yield float(node[0]), float(node[1])
        else:
            for child in node:
                yield from _pairs(child)


def meta_number(value: Any) -> int | None:
    raw = str(value if value is not None else '').strip()
    if not re.fullmatch(r'\d{1,3}', raw):
        return None
    n = int(raw)
    return n if n > 0 else None


def _is_public(feature: dict) -> bool:
    return str((feature.get('properties') or {}).get(PUBLIC_FLAG) or '').strip().casefold() == 'sim'


def layer_for(feature: dict) -> str:
    props = feature.get('properties') or {}
    expected = GEOM_LAYERS.get((feature.get('geometry') or {}).get('type'), '')
    declared = props.get('camada')
    if declared and declared not in ALLOWED_LAYERS:
        raise ValueError(f'Camada desconhecida: {declared}')
    if declared and declared != expected:
        raise ValueError('A camada declarada não corresponde à geometria.')
    return expected


def validate_geojson(path: Path) -> dict:
    if not path.is_file() or path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError('GeoJSON ausente ou maior que 30 MiB.')
    data = _read_json(path)
    if data.get('type') != 'FeatureCollection' or not isinstance(data.get('features'), list):
        raise ValueError('Arquivo deve ser GeoJSON FeatureCollection.')
    crs = data.get('crs')
    if crs and '4326' not in json.dumps(crs) and 'CRS84' not in json.dumps(crs):
        raise ValueError('GeoJSON deve usar WGS84 (EPSG:4326), longitude/latitude.')
    features = data['features']
    if not features:
        raise ValueError('GeoJSON não contém registros; publicação vazia bloqueada.')
    counts = Counter()
    all_counts = Counter()
    metas = set()
    for i, f in enumerate(features, 1):
        if not isinstance(f, dict) or f.get('type') != 'Feature' or not isinstance(f.get('properties'), dict):
            raise ValueError(f'Feição {i} inválida.')
        props = f['properties']
        if PUBLIC_FLAG not in props:
            raise ValueError(f'Feição {i}: falta a indicação explícita de publicação ({PUBLIC_FLAG}).')
        n = meta_number(props.get('Meta'))
        if n is None:
            raise ValueError(f'Feição {i}: número da Meta inválido ou ausente.')
        metas.add(n)
        geom = f.get('geometry')
        if not isinstance(geom, dict) or geom.get('type') not in GEOM_LAYERS:
            raise ValueError(f'Feição {i}: tipo de geometria não suportado.')
        pairs = list(_pairs(geom.get('coordinates')))
        if not pairs:
            raise ValueError(f'Feição {i}: geometria sem coordenadas.')
        # Sanidade para dados do município. Não substitui validação topológica QGIS.
        if any(not (math.isfinite(x) and math.isfinite(y) and -49 <= x <= -44 and -26 <= y <= -21)
               for x, y in pairs):
            raise ValueError(f'Feição {i}: coordenadas fora da região de SP ou inválidas.')
        lyr = layer_for(f)
        all_counts[lyr] += 1
        if _is_public(f):
            counts[lyr] += 1
    if not counts:
        raise ValueError('Nenhuma feição marcada como publicável. Upload bloqueado.')
    return {
        'total': len(features), 'publicaveis': sum(counts.values()),
        'camadas': dict(counts), 'camadas_totais': dict(all_counts), 'total_metas': len(metas),
    }


def validate_gpkg(path: Path, expected_counts: dict[str, int]) -> dict:
    if not path.is_file() or path.stat().st_size > MAX_GPKG_BYTES:
        raise ValueError('GeoPackage ausente ou maior que 120 MiB.')
    with path.open('rb') as f:
        if f.read(16) != b'SQLite format 3\x00':
            raise ValueError('GeoPackage não é SQLite válido.')
    # URI read-only + immutable: arquivo já foi gravado e nunca é modificado.
    conn = sqlite3.connect(path.as_uri() + '?mode=ro&immutable=1', uri=True)
    try:
        check = conn.execute('PRAGMA quick_check').fetchone()
        if check != ('ok',):
            raise ValueError('GeoPackage possui erros de integridade.')
        rows = conn.execute("SELECT table_name, data_type FROM gpkg_contents").fetchall()
        kinds = dict(rows)
        result = {}
        for lyr, expected in expected_counts.items():
            if lyr not in kinds or kinds[lyr] != 'features':
                raise ValueError(f'GeoPackage não possui a camada geográfica {lyr!r}.')
            actual = conn.execute(f'SELECT COUNT(*) FROM "{lyr}"').fetchone()[0]
            if actual != expected:
                raise ValueError(f'GeoJSON e GeoPackage divergem na camada {lyr}: {expected} / {actual}.')
            result[lyr] = actual
        return result
    except sqlite3.DatabaseError as exc:
        raise ValueError('GeoPackage inválido ou sem estrutura GPKG.') from exc
    finally:
        conn.close()


def _baseline() -> dict:
    if not BASE_JSON.is_file():
        raise FileNotFoundError('Arquivo base de 19/11/2026 não encontrado.')
    return {
        'id': BASE_ID, 'data_referencia': '2026-11-19', 'criado_em': '2026-11-19',
        'descricao': 'Versão inicial (arquivos distribuídos junto com o projeto)',
        'arquivo_geojson': BASE_JSON.name,
        'arquivo_gpkg': BASE_GPKG.name if BASE_GPKG.is_file() else None,
        'criado_por': None,
    }


def metadata_for(version_id: str) -> dict:
    if version_id == BASE_ID:
        return _baseline()
    folder = _version_dir(version_id)
    meta = _read_json(folder / 'metadata.json')
    if meta.get('id') != version_id or meta.get('arquivo_geojson') != 'camada.geojson':
        raise ValueError('Metadados da versão inconsistentes.')
    if not (folder / 'camada.geojson').is_file():
        raise FileNotFoundError('GeoJSON da versão arquivada não encontrado.')
    return meta


def _paths_for(version_id: str) -> tuple[Path, Path | None]:
    if version_id == BASE_ID:
        return BASE_JSON, BASE_GPKG if BASE_GPKG.is_file() else None
    base = _version_dir(version_id)
    gpkg = base / 'original.gpkg'
    return base / 'camada.geojson', gpkg if gpkg.exists() else None


def active_id() -> str:
    p = storage_dir() / 'active.json'
    if not p.is_file():
        return BASE_ID
    value = str(_read_json(p).get('id') or '')
    metadata_for(value)  # Fail-closed; não voltar silenciosamente para versão antiga.
    return value


def active_version() -> dict:
    return metadata_for(active_id())


def list_versions() -> list[dict]:
    versions = []
    if BASE_JSON.is_file():
        versions.append(_baseline())
    folder = _versions_dir()
    if folder.is_dir():
        for item in folder.iterdir():
            if item.is_dir() and _ID_RE.fullmatch(item.name):
                try:
                    versions.append(metadata_for(item.name))
                except (OSError, ValueError, KeyError):
                    continue
    current = active_id()
    versions.sort(key=lambda x: (x['data_referencia'], x['id']), reverse=True)
    return [{**v, 'ativa': v['id'] == current} for v in versions]


def create_draft(*, geojson_bytes: bytes, gpkg_bytes: bytes | None,
                 data_referencia: str, descricao: str, actor_id: int | None) -> dict:
    try:
        normalized = date.fromisoformat(data_referencia).isoformat()
    except (ValueError, TypeError) as exc:
        raise ValueError('Informe uma data válida no formato AAAA-MM-DD.') from exc
    if not geojson_bytes or len(geojson_bytes) > MAX_JSON_BYTES:
        raise ValueError('GeoJSON obrigatório, até 30 MiB.')
    if gpkg_bytes is not None and len(gpkg_bytes) > MAX_GPKG_BYTES:
        raise ValueError('GeoPackage deve ter até 120 MiB.')
    version_id = f'{normalized}-{uuid.uuid4().hex[:12]}'
    root = storage_dir()
    staging = root / ('.staging-' + uuid.uuid4().hex)
    staging.mkdir(parents=True, exist_ok=False)
    try:
        json_path = staging / 'camada.geojson'
        json_path.write_bytes(geojson_bytes)
        summary = validate_geojson(json_path)
        if gpkg_bytes is not None:
            gpkg_path = staging / 'original.gpkg'
            gpkg_path.write_bytes(gpkg_bytes)
            validate_gpkg(gpkg_path, summary['camadas_totais'])
        metadata = {
            'id': version_id, 'data_referencia': normalized,
            'criado_em': _now(), 'descricao': descricao.strip()[:500],
            'arquivo_geojson': 'camada.geojson',
            'arquivo_gpkg': 'original.gpkg' if gpkg_bytes is not None else None,
            'criado_por': actor_id, 'resumo': summary,
            'sha256_geojson': hashlib.sha256(geojson_bytes).hexdigest(),
            'sha256_gpkg': hashlib.sha256(gpkg_bytes).hexdigest() if gpkg_bytes is not None else None,
        }
        _write_atomic(staging / 'metadata.json', metadata)
        target = _version_dir(version_id)
        target.parent.mkdir(parents=True, exist_ok=True)
        with _LOCK:
            os.replace(staging, target)
        return metadata
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def _public_keys(data: dict) -> set[tuple]:
    result = set()
    for feature in data['features']:
        if not _is_public(feature):
            continue
        p = feature['properties']
        # Trecho diferencia as duas linhas da Meta 54.
        result.add((str(p.get('Meta')), str(p.get('Código')), str(p.get('Trecho') or ''),
                    layer_for(feature)))
    return result


def publish(version_id: str, actor_id: int | None, *, allow_missing: bool = False) -> dict:
    # Só deve ser chamado após checagem SITE_PUBLISH na camada Reflex.
    with _LOCK:
        meta = metadata_for(version_id)
        geojson_path, gpkg_path = _paths_for(version_id)
        summary = validate_geojson(geojson_path)
        if gpkg_path is not None and version_id != BASE_ID:
            validate_gpkg(gpkg_path, summary['camadas_totais'])
        candidate = _read_json(geojson_path)
        old_source, _ = active_geojson()
        missing = _public_keys(old_source) - _public_keys(candidate)
        if missing and not allow_missing:
            raise ValueError(
                f'A nova versão não contém {len(missing)} registros publicados atualmente. '
                'Confirme explicitamente a substituição com retirada desses registros '
                'ou escolha uma versão completa.'
            )
        _write_atomic(storage_dir() / 'active.json', {
            'id': version_id, 'publicada_em': _now(), 'publicada_por': actor_id,
            'registros_retirados_confirmados': len(missing) if allow_missing else 0,
        })
        return meta


def active_geojson() -> tuple[dict, dict]:
    try:
        version = active_version()
        geojson_path, _ = _paths_for(version['id'])
        signature = (str(geojson_path), geojson_path.stat().st_mtime_ns, geojson_path.stat().st_size)
        return _load_cached(*signature), version
    except (FileNotFoundError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=503, detail='Camadas GEO indisponíveis; confira os arquivos e a versão ativa.') from exc


@lru_cache(maxsize=8)
def _load_cached(path: str, _mtime_ns: int, _size: int) -> dict:
    data = _read_json(Path(path))
    if data.get('type') != 'FeatureCollection' or not isinstance(data.get('features'), list):
        raise ValueError('GeoJSON inválido.')
    return data


def public_collection(*, meta: int | None = None, camada: str | None = None) -> dict:
    source, version = active_geojson()
    public = []
    global_counts: Counter[str] = Counter()
    for f in source['features']:
        if not isinstance(f, dict) or not isinstance(f.get('properties'), dict):
            continue
        if not _is_public(f) or not isinstance(f.get('geometry'), dict):
            continue
        lyr = layer_for(f)
        global_counts[lyr] += 1
        if camada and lyr != camada:
            continue
        if meta is not None and meta_number(f['properties'].get('Meta')) != meta:
            continue
        public.append({
            'type': 'Feature', 'geometry': f['geometry'],
            'properties': {k: f['properties'][k] for k in PUBLIC_FIELDS if k in f['properties']},
        })
    return {
        'type': 'FeatureCollection', 'features': public,
        'metadata': {
            'fonte': version['arquivo_geojson'],
            'versao_ativa': version['id'],
            'data': version['data_referencia'], 'crs': 'EPSG:4326',
            'meta': f'{meta:02d}' if meta is not None else None,
            'camada': camada, 'total_retornado': len(public),
            'total_publicavel_na_fonte': sum(global_counts.values()),
            'camadas_publicaveis_na_fonte': dict(global_counts),
        },
    }


def public_info() -> dict:
    source, version = active_geojson()
    counts: Counter[str] = Counter()
    metas = set()
    for f in source['features']:
        if not isinstance(f, dict) or not _is_public(f):
            continue
        counts[layer_for(f)] += 1
        n = meta_number((f.get('properties') or {}).get('Meta'))
        if n is not None:
            metas.add(n)
    _, gpkg_path = _paths_for(version['id'])
    return {
        'fonte': 'camadas_geo_independentes',
        'versao_ativa': version['id'],
        'data': version['data_referencia'],
        'geojson': version['arquivo_geojson'],
        'geopackage': version['arquivo_gpkg'],
        'crs_geojson': 'EPSG:4326',
        'total_na_fonte': len(source['features']),
        'total_publicavel': sum(counts.values()),
        'camadas_publicaveis': dict(counts),
        'metas_publicaveis': [f'{n:02d}' for n in sorted(metas)],
        'download_gpkg_publico_habilitado': os.getenv('CMS_CAMADAS_GPKG_DOWNLOAD_PUBLICO','0').strip() == '1'
            and gpkg_path is not None,
    }


def public_gpkg_path() -> Path:
    if os.getenv('CMS_CAMADAS_GPKG_DOWNLOAD_PUBLICO','0').strip() != '1':
        raise HTTPException(status_code=403, detail='Download público do GeoPackage desabilitado.')
    try:
        _, path = _paths_for(active_id())
        if path is None or not path.exists():
            raise FileNotFoundError('GeoPackage não disponível.')
        return path
    except (OSError, ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=503, detail='GeoPackage da versão ativa não disponível.') from exc
