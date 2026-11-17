"""GeoJSON/WKT e coordenadas. Não geocodifica nem inventa localização.

Suporta tipos encontrados no CSV: Point, MultiLineString, MultiPolygon,
mais LineString, Polygon e MultiPoint para cadastro manual posterior.
"""
from __future__ import annotations

import math
import re
from typing import Any

_NUMBER = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")
_TYPES = {
    "POINT": ("Point", 0),
    "LINESTRING": ("LineString", 1),
    "POLYGON": ("Polygon", 2),
    "MULTIPOINT": ("MultiPoint", 1),
    "MULTILINESTRING": ("MultiLineString", 2),
    "MULTIPOLYGON": ("MultiPolygon", 3),
}
# Envelope amplo de SP usado somente como checagem de sanidade, não como
# geometria oficial da cidade.
LIMITS = (-47.3, -24.2, -45.8, -23.1)


def _read_numbers(text: str, index: int) -> tuple[list[float], int]:
    values: list[float] = []
    while True:
        match = _NUMBER.match(text, index)
        if match is None:
            break
        number = float(match.group())
        if not math.isfinite(number):
            raise ValueError("Valor de coordenada não finito")
        values.append(number)
        index = match.end()
        while index < len(text) and text[index].isspace():
            index += 1
    if len(values) != 2:
        raise ValueError("Esperadas duas coordenadas WGS84 (longitude latitude)")
    return values, index


def _parse_nested(text: str, index: int) -> tuple[Any, int]:
    while index < len(text) and text[index].isspace():
        index += 1
    if index >= len(text) or text[index] != "(":
        return _read_numbers(text, index)
    index += 1
    items = []
    while True:
        while index < len(text) and text[index].isspace():
            index += 1
        item, index = _parse_nested(text, index)
        items.append(item)
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            raise ValueError("WKT incompleto")
        if text[index] == ")":
            return items, index + 1
        if text[index] != ",":
            raise ValueError(f"Separador WKT inválido na posição {index}")
        index += 1


def _coord_depth(value: Any) -> int:
    if isinstance(value, list) and len(value) == 2 and all(isinstance(v, (int, float)) for v in value):
        return 0
    if isinstance(value, list) and value:
        child_depths = {_coord_depth(x) for x in value}
        if len(child_depths) != 1:
            raise ValueError("Estrutura WKT irregular")
        return next(iter(child_depths)) + 1
    raise ValueError("Estrutura WKT vazia/inválida")


def parse_wkt(text: str) -> dict[str, Any]:
    """Converte WKT para GeoJSON sem dependência adicional.

    Não aceita CRS arbitrário, Z/M, SRID ou EMPTY; evita interpretações
    geográficas silenciosas de dados que exigiriam um conversor de projeção.
    """
    match = re.match(r"^\s*([A-Za-z]+)\s*", text)
    if not match or match.group(1).upper() not in _TYPES:
        raise ValueError("Tipo de WKT não suportado")
    geo_type, expected_depth = _TYPES[match.group(1).upper()]
    data, end = _parse_nested(text, match.end())
    if text[end:].strip():
        raise ValueError("Caracteres extras no WKT")
    if geo_type == "Point" and isinstance(data, list) and len(data) == 1:
        data = data[0]
    if geo_type == "MultiPoint" and isinstance(data, list):
        data = [entry[0] if isinstance(entry, list) and len(entry) == 1 and _coord_depth(entry) == 1 else entry
                for entry in data]
    depth = _coord_depth(data)
    if depth != expected_depth:
        # Convenção WKT MULTIPOINT aceita (x y, x y), tratada pelo parser.
        raise ValueError(f"Estrutura de {geo_type} incorreta: profundidade {depth}")
    return {"type": geo_type, "coordinates": data}


def all_coordinates(coords: Any):
    if isinstance(coords, (list, tuple)) and len(coords) >= 2 and all(
        isinstance(x, (float, int)) for x in coords[:2]
    ):
        yield float(coords[0]), float(coords[1])
        return
    if isinstance(coords, (list, tuple)):
        for elem in coords:
            yield from all_coordinates(elem)


def valid_sp_geometry(geom: dict[str, Any]) -> bool:
    points = list(all_coordinates(geom.get("coordinates", [])))
    min_lng, min_lat, max_lng, max_lat = LIMITS
    return bool(points) and all(
        math.isfinite(lng) and math.isfinite(lat)
        and min_lng <= lng <= max_lng and min_lat <= lat <= max_lat
        for lng, lat in points
    )


def point_from_values(latitude: Any, longitude: Any) -> dict[str, Any] | None:
    try:
        lat = float(str(latitude).strip().replace(",", "."))
        lng = float(str(longitude).strip().replace(",", "."))
    except (TypeError, ValueError):
        return None
    geom = {"type": "Point", "coordinates": [lng, lat]}
    return geom if valid_sp_geometry(geom) else None


def geometry_from_payload(data: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    raw_wkt = str(data.get("Geometria_WKT") or "").strip()
    if raw_wkt:
        try:
            geom = parse_wkt(raw_wkt)
            if valid_sp_geometry(geom):
                return geom, "wkt"
            return None, "wkt_fora_area"
        except (ValueError, RecursionError):
            return None, "wkt_invalido"
    geom = point_from_values(data.get("Latitude"), data.get("Longitude"))
    if geom:
        return geom, "coordenadas"
    return None, "sem_geometria_confiavel"
