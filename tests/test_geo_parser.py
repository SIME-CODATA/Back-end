"""Testes sem PostgreSQL e sem inicializar a aplicação Reflex."""
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path

# As dependências do app não são necessárias para validar a leitura fiel.
code_name = "Back_end.site_cms.modules.metas.code"
code = types.ModuleType(code_name)
def canonical(value):
    raw = str(value or "").strip()
    return f"{int(raw):02d}" if raw.isdigit() and int(raw) < 10 else (str(int(raw)) if raw.isdigit() else raw)
code.canonical_meta_code = canonical
sys.modules[code_name] = code
file = Path(__file__).resolve().parents[1] / "Back_end/site_cms/modules/metas/geografia/parser.py"
spec = importlib.util.spec_from_file_location("geo_parser_for_tests", file)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ParserTest(unittest.TestCase):
    def test_csv_all_rows_and_all_19_columns(self):
        path = Path(__file__).parents[1] / "data/base_geo_2026(02_GESTAO_MONITORES).csv"
        rows = mod.read_records(path)
        audit = mod.audit_records(rows)
        self.assertEqual(len(rows), 681)
        self.assertEqual(audit["metas_cobertas"], 88)
        self.assertEqual(len(rows[0]["payload"]), 19)
        self.assertEqual(sum(bool(r["payload"]["Geometria_WKT"]) for r in rows), 27)
        self.assertEqual(len(set(r["source_key"] for r in rows)), 681)
        self.assertEqual(len([r for r in rows if r["external_code"] == "11.01.25.01"]), 2)
        self.assertEqual(len([r for r in rows if r["external_code"] == "11.01.25.01" and r["meta_code"] == "11"]), 2)

    def test_json_preserves_new_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.json"
            path.write_text(json.dumps({"records": [{"codigo": "01.99.01", "Meta": "1",
                "Descrição Projeto": "Ponte", "Campo futuro": {"valor": 123, "itens": ["a", "b"]}}]}), encoding="utf-8")
            rows = mod.read_records(path, "json")
            self.assertEqual(rows[0]["meta_code"], "01")
            self.assertEqual(rows[0]["payload"]["Campo futuro"], {"valor": 123, "itens": ["a", "b"]})

    def test_public_filters_sensitive_fields(self):
        entry = {"Meta": "1", "codigo": "1.1", "Latitude": "-23.5", "Longitude": "-46.5",
                 "Observações adicionais": "Não divulgar", "Geometria_WKT": "Point(...)"}
        public = mod.safe_public_payload(entry)
        self.assertNotIn("Observações adicionais", public)
        self.assertNotIn("Geometria_WKT", public)
        self.assertEqual(public["latitude"], -23.5)
        self.assertEqual(public["longitude"], -46.5)


if __name__ == "__main__":
    unittest.main()
