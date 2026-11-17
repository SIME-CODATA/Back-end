"""Auditoria offline sem tocar no banco. Exemplo:
uv run python -m Back_end.site_cms.modules.metas.fontes_cli --auditoria
uv run python -m Back_end.site_cms.modules.metas.fontes_cli --separar-abas
uv run python -m Back_end.site_cms.modules.metas.fontes_cli --meta 01
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from .fontes_leitor import DATA_DIR, all_sheets, audit, for_meta
from .fontes_mapa import geojson_meta


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Gerado:", path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auditoria", action="store_true", help="Salva relatório de cobertura e SHA-256")
    parser.add_argument("--separar-abas", action="store_true", help="Gera JSON derivado por aba, sem alterar Excel/CSV")
    parser.add_argument("--meta", default=None, help="Exibe cobertura e geometrias de uma meta")
    args = parser.parse_args()
    report = audit()
    print(json.dumps({k: v for k, v in report.items() if k != "fontes"}, ensure_ascii=False, indent=2))
    if args.auditoria:
        write_json(DATA_DIR / "gerados" / "AUDITORIA_FONTES.json", report)
    if args.separar_abas:
        base = DATA_DIR / "gerados" / "abas"
        for idx, sheet in enumerate(all_sheets(), start=1):
            name = re.sub(r"[^\w-]+", "_", sheet["aba"], flags=re.U).strip("_")[:70] or "aba"
            write_json(base / f"{idx:02d}_{name}.json", sheet)
    if args.meta is not None:
        obj = for_meta(args.meta)
        geo = geojson_meta(args.meta)
        print(json.dumps({"codigo": obj["codigo"], "total_registros": obj["total_registros"],
                          "abas": [{"nome": s["aba"], "linhas": s["total"]} for s in obj["abas"]],
                          "geografia": geo["metadata"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
