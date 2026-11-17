"""Leitura somente leitura de TODAS as abas XLSX/CSV do CMS de Metas.

Nenhum arquivo em data/ é alterado. Linhas totalmente vazias são ignoradas
na visão indexada; as originais, incluindo espaçadores, continuam intocadas.
O campo 'Meta' é usado para vincular linhas às 132 metas, SEM inferências.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import posixpath
import re
import unicodedata
import zipfile
from functools import lru_cache
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

DATA_DIR = Path(__file__).resolve().parent / "data"
GEO_FILES = {
    "metas": "metas.geojson",
    "mascara": "sao-paulo-mascara.geojson",
    "subprefeituras": "subprefeituras(3).geojson",
}
MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
SPREADSHEET_PREFIX = ("meta", "numero da meta", "numero meta", "n da meta", "codigo da meta", "codigo meta", "meta_code")

# Cabeçalhos reais no XLSX fornecido. Não altera nem reordena uma célula.
KNOWN_HEADER_ROWS = {
    "00_GUIA_USO": 4,
    "02_GESTAO_MONITORES": 4,
    "ESPECIAL PREF. PRESENTE": 1,
    "03_GEO_PDM": 1,
    "06_COROP_PLANEJADOS": 1,
    "04_COROP_ZONAS": 1,
    "05_COROP_EXECUTADO": 1,
    "07_DICIONARIO": 4,
    "08_RELACAO_MAPAS": 1,
    "09_BUFFER_150M": 1,
    "99_LISTAS": 1,
    "input_QGIS": 1,
}
# São referências para qualquer meta. Não faz sentido replicá-las 132 vezes.
GLOBAL_REFERENCE_SHEETS = frozenset({
    "00_GUIA_USO", "01_GOVERNANCA_DADOS", "07_DICIONARIO", "99_LISTAS"
})
ACTION_CODE_SHEETS = frozenset({"02_GESTAO_MONITORES", "input_QGIS"})
ACTION_DEPENDENT_SHEETS = {"03_GEO_PDM": "Geocodigo", "09_BUFFER_150M": "geocodigo"}
MATRIX_SHEETS = frozenset({"04_COROP_ZONAS", "05_COROP_EXECUTADO", "06_COROP_PLANEJADOS"})


def _key(value: Any) -> str:
    value = unicodedata.normalize("NFKD", str(value or "").casefold())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in value if not unicodedata.combining(c))).strip()


def meta_code(value: Any) -> str | None:
    """Aceita somente número explícito 1..132 ou 'Meta 01'. Não adivinha."""
    value = str(value or "").strip()
    matched = re.fullmatch(r"(?:meta\s*(?:n[º°.]?\s*)?)?0*(\d{1,3})(?:\.0)?", value, re.I)
    if not matched:
        return None
    integer = int(matched.group(1))
    if not 1 <= integer <= 132:
        return None
    return f"{integer:02d}" if integer < 10 else str(integer)


def _col_name(n: int) -> str:
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _col_number(cell_ref: str) -> int:
    letters = re.match(r"[A-Za-z]+", cell_ref)
    if not letters:
        raise ValueError(f"Referencia de celula invalida: {cell_ref}")
    n = 0
    for c in letters.group().upper():
        n = n * 26 + ord(c) - 64
    return n


def _decode_csv(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            pass
    raise ValueError(f"CSV com codificacao nao reconhecida: {path.name}")


def _rows_csv(path: Path) -> list[dict[str, Any]]:
    text = _decode_csv(path)
    # Sniffer falha em arquivos com grandes capas/celulas de espaco; fallback comma.
    try:
        dialect = csv.Sniffer().sniff(text[:16000], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rows: list[dict[str, Any]] = []
    for number, values in enumerate(csv.reader(io.StringIO(text, newline=""), dialect), start=1):
        cells = {_col_name(i): v for i, v in enumerate(values, start=1) if v.strip()}
        if cells:
            rows.append({"linha": number, "celulas": cells, "formulas": {}})
    return rows


def _xlsx_shared_strings(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in el.iter(f"{{{MAIN}}}t")) for el in root.findall(f"{{{MAIN}}}si")]


def _xlsx_sheets(path: Path) -> list[tuple[str, list[dict[str, Any]]]]:
    result = []
    with zipfile.ZipFile(path) as z:
        shared = _xlsx_shared_strings(z)
        book = ET.fromstring(z.read("xl/workbook.xml"))
        rels_root = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        relations = {r.attrib["Id"]: r.attrib["Target"] for r in rels_root.findall(f"{{{PKG_REL}}}Relationship")}
        for sheet in book.findall(f"{{{MAIN}}}sheets/{{{MAIN}}}sheet"):
            name = sheet.attrib["name"]
            rid = sheet.attrib.get(f"{{{REL}}}id", "")
            target = relations.get(rid)
            if not target:
                raise ValueError(f"Aba {name!r} sem relacionamento XLSX")
            dest = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
            if not dest.startswith("xl/worksheets/") or ".." in dest.split("/"):
                raise ValueError(f"Caminho de aba invalido: {dest}")
            worksheet = ET.fromstring(z.read(dest))
            rows = []
            for row in worksheet.findall(f".//{{{MAIN}}}sheetData/{{{MAIN}}}row"):
                cells: dict[str, str] = {}
                formulas: dict[str, str] = {}
                for cell in row.findall(f"{{{MAIN}}}c"):
                    col = re.match(r"[A-Za-z]+", cell.attrib.get("r", ""))
                    if col is None:
                        continue
                    key = col.group().upper()
                    cell_type = cell.attrib.get("t", "")
                    v = cell.find(f"{{{MAIN}}}v")
                    f = cell.find(f"{{{MAIN}}}f")
                    if f is not None and f.text:
                        formulas[key] = "=" + f.text
                    if cell_type == "inlineStr":
                        inline = cell.find(f"{{{MAIN}}}is")
                        value = "" if inline is None else "".join(x.text or "" for x in inline.iter(f"{{{MAIN}}}t"))
                    elif cell_type == "s" and v is not None and v.text is not None:
                        value = shared[int(v.text)]
                    elif cell_type == "b" and v is not None:
                        value = "TRUE" if v.text == "1" else "FALSE"
                    else:
                        # Preserva o valor armazenado pelo Excel. Formula sem cache
                        # permanece visivel como formula e e reportada em 'formulas'.
                        value = v.text if v is not None and v.text is not None else formulas.get(key, "")
                    if value != "" and value is not None and str(value).strip():
                        cells[key] = str(value)
                if cells or formulas:
                    rows.append({"linha": int(row.attrib["r"]), "celulas": cells, "formulas": formulas})
            result.append((name, rows))
    return result


def _is_header(cells: dict[str, str]) -> bool:
    values = [_key(v) for v in cells.values()]
    has_meta = "meta" in values or any(v in SPREADSHEET_PREFIX for v in values)
    has_other = any(v in {"codigo", "eixo", "indicador", "descricao projeto", "secretaria", "acao", "situacao", "subprefeitura"} for v in values)
    return has_meta and has_other and len(values) >= 2


def _to_records(name: str, origin: str, raw_rows: list[dict[str, Any]]) -> dict[str, Any]:
    # Quando nao houver cabecalho identificado, NENHUMA linha e jogada fora.
    current_headers: dict[str, str] = {}
    header_line = None
    rows = []
    count_meta = 0
    for row in raw_rows:
        cells = row["celulas"]
        if _is_header(cells) or row["linha"] == KNOWN_HEADER_ROWS.get(name):
            current_headers = dict(cells)
            header_line = row["linha"]
            rows.append({**row, "campos": {}, "meta": None, "tipo": "cabecalho"})
            continue
        fields = {}
        for column, value in cells.items():
            label = current_headers.get(column, "")
            if label:
                key = label
                if key in fields:
                    key = f"{label} [{column}]"
                fields[key] = value
        # As colunas de cabecalho com valor vazio continuam presentes como "".
        for column, label in current_headers.items():
            if label and label not in fields:
                fields[label] = ""
        linked = None
        for label, value in fields.items():
            if _key(label) in SPREADSHEET_PREFIX:
                linked = meta_code(value)
                if linked:
                    break
        if not linked:
            # Aba individual 'Meta 01' pode nao ter coluna Meta.
            match = re.fullmatch(r"\s*meta\s*(?:n[º°.]?\s*)?(\d{1,3})\s*", name, re.I)
            if match:
                linked = meta_code(match.group(1))
        if linked:
            count_meta += 1
        rows.append({**row, "campos": fields, "meta": linked, "tipo": "dado"})
    return {
        "arquivo": origin, "aba": name, "cabecalho_linha": header_line,
        "linhas_nao_vazias": len(raw_rows), "linhas_vinculadas": count_meta,
        "linhas": rows,
    }


def _source_files() -> list[Path]:
    excel = sorted(p for p in DATA_DIR.glob("*") if p.suffix.lower() in {".xlsx", ".xlsm"} and not p.name.startswith("~$"))
    # Nao duplica as linhas: com Excel original presente, ele e a fonte primária.
    if excel:
        return excel
    return sorted(DATA_DIR.glob("*.csv")) + sorted((DATA_DIR / "abas").glob("*.csv"))


def _signature() -> tuple:
    files = _source_files()
    return tuple((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in files)


@lru_cache(maxsize=4)
def _load(signature: tuple) -> tuple[dict[str, Any], ...]:
    sheets = []
    for filename, _, _ in signature:
        path = Path(filename)
        if path.suffix.lower() == ".csv":
            sheets.append(_to_records(path.stem, path.name, _rows_csv(path)))
        else:
            for sheetname, raw in _xlsx_sheets(path):
                sheets.append(_to_records(sheetname, path.name, raw))
    return tuple(sheets)


def all_sheets() -> tuple[dict[str, Any], ...]:
    return _load(_signature())


def _action_lookup(sheets: tuple[dict[str, Any], ...]) -> dict[str, set[str]]:
    """Índice oficial código da ação -> meta, não baseado no nome da obra."""
    lookup: dict[str, set[str]] = {}
    for sheet in sheets:
        if sheet["aba"] not in ACTION_CODE_SHEETS:
            continue
        for row in sheet["linhas"]:
            code = str(row.get("campos", {}).get("codigo", "")).strip().casefold()
            if code and row.get("meta"):
                lookup.setdefault(code, set()).add(row["meta"])
    return lookup


def _row_links(sheet: dict[str, Any], row: dict[str, Any],
               action_lookup: dict[str, set[str]]) -> dict[str, dict[str, str]]:
    """Regras explícitas por aba. Conflitos/ausências não são adivinhados."""
    if row.get("tipo") != "dado":
        return {}
    name = sheet["aba"]
    if name in GLOBAL_REFERENCE_SHEETS:
        return {}
    if row.get("meta"):
        return {row["meta"]: {"tipo": "meta_explicita", "coluna": "", "chave": row["meta"]}}
    fields = row.get("campos", {})
    if name in ACTION_DEPENDENT_SHEETS:
        code = str(fields.get(ACTION_DEPENDENT_SHEETS[name], "")).strip().casefold()
        matches = action_lookup.get(code, set())
        if len(matches) == 1:
            canonical = next(iter(matches))
            return {canonical: {"tipo": "codigo_acao", "coluna": ACTION_DEPENDENT_SHEETS[name], "chave": code}}
        return {}
    if name in MATRIX_SHEETS:
        result: dict[str, dict[str, str]] = {}
        for column, label in _column_labels(sheet).items():
            m = re.fullmatch(r"meta[ _]+0*(\d{1,3})", str(label), re.I)
            if not m or column not in row["celulas"]:
                continue  # Vazio = sem valor; zero explícito é preservado.
            canonical = meta_code(m.group(1))
            if canonical:
                result[canonical] = {
                    "tipo": "coluna_meta", "coluna": column,
                    "campo": label, "valor": row["celulas"][column],
                }
        return result
    return {}


def _column_labels(sheet: dict[str, Any]) -> dict[str, str]:
    """Obtém a linha de cabeçalho preservada, inclusive em matrizes COROP."""
    for row in sheet["linhas"]:
        if row["tipo"] == "cabecalho":
            return row["celulas"]
    return {}


def _related(sheets: tuple[dict[str, Any], ...]):
    actions = _action_lookup(sheets)
    linked = []
    for sheet in sheets:
        rows = [(row, _row_links(sheet, row, actions)) for row in sheet["linhas"]]
        linked.append((sheet, rows))
    return linked


def for_meta(code: str | int) -> dict[str, Any]:
    canonical = meta_code(code)
    if canonical is None:
        raise ValueError(f"Numero de Meta invalido: {code!r}")
    sections = []
    globals_summary = []
    for sheet, rows in _related(all_sheets()):
        is_global = sheet["aba"] in GLOBAL_REFERENCE_SHEETS
        if is_global:
            globals_summary.append({"aba": sheet["aba"], "arquivo": sheet["arquivo"],
                                    "linhas_nao_vazias": sheet["linhas_nao_vazias"]})
        linked = [
            {**row, "meta": canonical, "vinculo": relations[canonical]}
            for row, relations in rows if canonical in relations
        ]
        sections.append({
            "arquivo": sheet["arquivo"], "aba": sheet["aba"],
            "tipo": "referencia_global" if is_global else "dados_da_meta",
            "total": len(linked), "linhas": linked,
        })
    return {"codigo": canonical, "total_abas": len(sections),
            "total_registros": sum(section["total"] for section in sections),
            "abas": sections, "referencias_globais": globals_summary}


def audit() -> dict[str, Any]:
    sheets = all_sheets()
    metas = set()
    stats = []
    orphan_examples = []
    for sheet, rows in _related(sheets):
        is_global = sheet["aba"] in GLOBAL_REFERENCE_SHEETS
        linked_rows = 0
        links = 0
        unlinked = 0
        header_count = 0
        for row, relations in rows:
            if row["tipo"] == "cabecalho":
                header_count += 1
            elif not is_global:
                if relations:
                    linked_rows += 1
                    links += len(relations)
                    metas.update(relations)
                else:
                    unlinked += 1
                    if len(orphan_examples) < 50:
                        orphan_examples.append({
                            "aba": sheet["aba"], "linha": row["linha"],
                            "celulas": row["celulas"],
                        })
        stats.append({
            "arquivo": sheet["arquivo"], "aba": sheet["aba"],
            "tipo": "referencia_global" if is_global else "dados_da_meta",
            "linhas_nao_vazias": sheet["linhas_nao_vazias"],
            "linhas_vinculadas": linked_rows, "vinculos_metas": links,
            "linhas_sem_meta": unlinked, "linhas_cabecalho": header_count,
        })
    files = []
    for path in list(_source_files()) + [DATA_DIR / n for n in GEO_FILES.values()]:
        if path.is_file():
            files.append({"nome": path.name, "bytes": path.stat().st_size,
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    geo = {}
    for key in GEO_FILES:
        try:
            features = load_geojson(key).get("features", [])
            geo[key] = {"features": len(features),
                        "tipos": sorted({f.get("geometry", {}).get("type", "") for f in features})}
        except (OSError, ValueError) as error:
            geo[key] = {"erro": str(error)}
    return {
        "origem_planilha": "Excel (todas as abas)" if any(
            p.suffix.lower() in {".xlsx", ".xlsm"} for p in _source_files()) else "CSV (uma aba por arquivo)",
        "total_abas": len(sheets), "metas_cobertas": len(metas),
        "codigos_metas": sorted(metas, key=int), "abas": stats,
        "fontes": files, "geojson": geo, "pendencias_exemplos": orphan_examples,
        "observacao": "Matrizes COROP vinculadas pela coluna da meta; GEO e BUFFER pelo código da ação; referências globais não replicadas nas fichas. Original intacto.",
    }


@lru_cache(maxsize=9)
def _read_geo(name: str, mtime: int, size: int) -> dict[str, Any]:
    path = DATA_DIR / GEO_FILES[name]
    obj = json.loads(path.read_text(encoding="utf-8-sig"))
    if obj.get("type") != "FeatureCollection" or not isinstance(obj.get("features"), list):
        raise ValueError(f"GeoJSON invalido: {path.name}")
    return obj


def load_geojson(name: str) -> dict[str, Any]:
    if name not in GEO_FILES:
        raise ValueError("Camada inexistente")
    path = DATA_DIR / GEO_FILES[name]
    stat = path.stat()
    return _read_geo(name, stat.st_mtime_ns, stat.st_size)
