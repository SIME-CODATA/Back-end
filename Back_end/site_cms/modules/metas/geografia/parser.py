"""Leitura lossless de CSV CP1252/UTF-8, JSON e planilhas XLSX.

O CSV recebido contém três linhas de capa, cabeçalho na 4ª linha e 119
colunas vazias. O campo 'codigo' identifica uma AÇÃO, não a ficha da Meta;
'Meta' (1..132) é o vínculo com cms_meta_contents.
"""
from __future__ import annotations

import csv
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from Back_end.site_cms.modules.metas.code import canonical_meta_code

COLUMNS = (
    "codigo", "Meta", "Eixo", "Indicador", "Descrição Projeto", "Secretaria",
    "Status Regionalização", "Estágio da Ação", "Meta é regionalizável?",
    "Já tem local(is) definido(s)?", "Localização é públicável?",
    "Subprefeitura", "Distrito", "Endereço", "Latitude", "Longitude",
    "Observações adicionais", "Geometria_WKT", "Distrito_Primeira_Ocorrencia",
)
IDENTITY_FIELDS = {"Meta", "codigo"}
PUBLIC_FLAG = "Localização é públicável?"  # Grafia EXATA do arquivo recebido.


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Sim" if value else "Não"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _canonical_or_error(value: Any) -> str:
    code = canonical_meta_code(_as_text(value))
    if not code.isdigit() or not 1 <= int(code) <= 132:
        raise ValueError(f"Identificador de Meta inválido: {value!r}")
    return code


def _is_header(row: list[str]) -> bool:
    return len(row) >= 2 and row[0].strip().casefold() == "codigo" and row[1].strip() == "Meta"


def _from_table(rows: Iterable[list[Any]], *, label: str) -> list[dict[str, str]]:
    headers: list[str] | None = None
    result: list[dict[str, str]] = []
    for line, cells in enumerate(rows, start=1):
        vals = [_as_text(value) for value in cells]
        if headers is None:
            if _is_header(vals):
                headers = vals
                missing = [c for c in COLUMNS if c not in headers]
                if missing:
                    raise ValueError(f"Cabeçalho incompleto em {label}: {missing}")
            continue
        if not vals or not vals[0].strip():
            continue
        # Preserva também quaisquer colunas extras que possuam CABEÇALHO,
        # sem criar 119 campos vazios sem rótulo.
        record = {key: vals[i] if i < len(vals) else ""
                  for i, key in enumerate(headers) if key}
        record["__sheet_row__"] = str(line)
        result.append(record)
    if headers is None:
        raise ValueError(f"Não foi encontrado o cabeçalho 'codigo,Meta' em {label}.")
    return result


def _read_csv(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        content = raw.decode("cp1252")
    return _from_table(csv.reader(io.StringIO(content, newline="")), label=str(path))


def _read_xlsx(path: Path) -> list[dict[str, str]]:
    try:
        from openpyxl import load_workbook
    except ImportError as error:
        raise RuntimeError("Para importar XLSX, execute: uv add openpyxl") from error
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        for sheet in wb:
            # Suporta aba 'Gestão Controle Monitores' ou qualquer aba com cabeçalho.
            first = list(sheet.iter_rows(min_row=1, max_row=25, values_only=True))
            if any(_is_header([_as_text(v) for v in row]) for row in first):
                return _from_table(sheet.iter_rows(values_only=True), label=f"{path}:{sheet.title}")
    finally:
        wb.close()
    raise ValueError("Nenhuma aba XLSX contém o cabeçalho de monitoramento.")


def _read_json(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(payload, dict):
        payload = payload.get("records", payload.get("registros", payload.get("rows")))
    if not isinstance(payload, list):
        raise ValueError("JSON deve ser uma lista ou conter 'records'/'registros'/'rows'.")
    result = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Registro JSON {index} não é um objeto.")
        row = item.get("data", item)
        if not isinstance(row, dict):
            raise ValueError(f"Campo 'data' inválido no registro JSON {index}.")
        if "Meta" not in row or "codigo" not in row:
            raise ValueError(f"JSON registro {index} precisa de 'Meta' e 'codigo'.")
        # JSONB preserva os tipos originais, inclusive objetos e listas adicionais.
        result.append({**{str(k): v for k, v in row.items()}, "__sheet_row__": str(index)})
    return result


def read_records(path: str | Path, source: str = "planilha") -> list[dict[str, Any]]:
    """Normaliza identidade da linha, mas preserva TODOS os valores originais.

    Repetições de código são distinguidas por ocorrência, sem perda de linha.
    """
    if source not in {"planilha", "json", "smae"}:
        raise ValueError("source deve ser planilha, json ou smae")
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":
        original = _read_csv(path)
    elif ext in {".xlsx", ".xlsm"}:
        original = _read_xlsx(path)
    elif ext == ".json":
        original = _read_json(path)
    else:
        raise ValueError("Formato não aceito. Utilize .csv, .xlsx/.xlsm ou .json.")

    occurrences: dict[tuple[str, str], int] = defaultdict(int)
    result: list[dict[str, Any]] = []
    for record in original:
        sheet_row = int(record.pop("__sheet_row__", "0"))
        meta_code = _canonical_or_error(record.get("Meta", ""))
        external_code = _as_text(record.get("codigo", "")).strip()
        if not external_code:
            raise ValueError(f"Linha {sheet_row} sem codigo de ação")
        token = (meta_code, external_code)
        occurrences[token] += 1
        source_key = f"{source}:{meta_code}:{external_code}:{occurrences[token]}"
        result.append({
            "meta_code": meta_code,
            "external_code": external_code,
            "source": source,
            "source_key": source_key,
            "sheet_row": sheet_row,
            "payload": record,
        })
    return result


def _coordinate(raw: str, *, latitude: bool) -> float | None:
    value = raw.strip().replace(",", ".")
    if not value:
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    limit = 90 if latitude else 180
    return parsed if -limit <= parsed <= limit else None


def audit_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Diagnóstico estático sem tocar no banco."""
    issues = []
    public_yes = 0
    with_coordinates = 0
    with_wkt = 0
    for row in records:
        data = row["payload"]
        lat = _as_text(data.get("Latitude", ""))
        lng = _as_text(data.get("Longitude", ""))
        if _as_text(data.get(PUBLIC_FLAG, "")).strip().casefold() == "sim":
            public_yes += 1
        if lat or lng:
            if _coordinate(lat, latitude=True) is not None and _coordinate(lng, latitude=False) is not None:
                with_coordinates += 1
                # Apenas alerta. Não substituímos localização declarada por outra.
                if not (-24.2 <= float(lat.replace(",", ".")) <= -23.1
                        and -47.3 <= float(lng.replace(",", ".")) <= -45.8):
                    issues.append({"linha": row["sheet_row"], "codigo": row["external_code"], "tipo": "coordenada_fora_area_sp"})
            else:
                issues.append({"linha": row["sheet_row"], "codigo": row["external_code"], "tipo": "coordenada_invalida"})
        if _as_text(data.get("Geometria_WKT", "")).strip():
            with_wkt += 1
    return {
        "registros": len(records),
        "metas_cobertas": len(set(item["meta_code"] for item in records)),
        "com_coordenadas_validas": with_coordinates,
        "com_geometria_wkt": with_wkt,
        "sinalizados_publicaveis_na_origem": public_yes,
        "codigos_repetidos": {f"{meta}/{codigo}": total for (meta, codigo), total in Counter((r["meta_code"],r["external_code"]) for r in records).items() if total > 1},
        "avisos": issues,
    }


def safe_public_payload(data: dict[str, str]) -> dict[str, Any]:
    """Apenas campos autorizados à vitrine pública; notas internas excluídas."""
    kept = {
        "codigo": "codigo", "Meta": "meta", "Eixo": "eixo",
        "Indicador": "indicador", "Descrição Projeto": "descricao_projeto",
        "Secretaria": "secretaria", "Status Regionalização": "status_regionalizacao",
        "Estágio da Ação": "estagio_acao", "Meta é regionalizável?": "meta_regionalizavel",
        "Já tem local(is) definido(s)?": "locais_definidos",
        PUBLIC_FLAG: "localizacao_publicavel", "Subprefeitura": "subprefeitura",
        "Distrito": "distrito", "Endereço": "endereco",
        "Distrito_Primeira_Ocorrencia": "distrito_primeira_ocorrencia",
    }
    result = {target: data.get(key, "") for key, target in kept.items()}
    latitude = _coordinate(_as_text(data.get("Latitude", "")), latitude=True)
    longitude = _coordinate(_as_text(data.get("Longitude", "")), latitude=False)
    # Não fornecer pins suspeitos ao mapa; a coordenada original fica no CMS.
    if (latitude is None or longitude is None or
            not (-24.2 <= latitude <= -23.1 and -47.3 <= longitude <= -45.8)):
        result["latitude"], result["longitude"] = None, None
        result["coordenadas_para_revisao"] = bool(data.get("Latitude") or data.get("Longitude"))
    else:
        result["latitude"], result["longitude"] = latitude, longitude
        result["coordenadas_para_revisao"] = False
    # NOTA: Geometria_WKT e Observações adicionais ficam SOMENTE no CMS.
    return result
