"""Testes de leitura dos arquivos enviados, sem Reflex/Postgres."""
import unittest
from Back_end.site_cms.modules.metas.fontes_leitor import all_sheets, audit, for_meta, load_geojson
from Back_end.site_cms.modules.metas.fontes_mapa import geojson_meta, public_spreadsheet


class FontesOffline(unittest.TestCase):
    def test_csv_completo(self):
        result = audit()
        self.assertEqual(result["total_abas"], 1)
        self.assertEqual(result["metas_cobertas"], 88)
        self.assertEqual(result["abas"][0]["linhas_vinculadas"], 681)
        self.assertEqual(result["abas"][0]["linhas_nao_vazias"], 684)

    def test_meta_01(self):
        meta = for_meta("01")
        self.assertEqual(meta["total_registros"], 23)
        first = next(row for row in meta["abas"][0]["linhas"] if row["campos"].get("codigo") == "01.00.01")
        self.assertEqual(first["linha"], 6)
        self.assertIn("Observações adicionais", first["campos"])
        self.assertEqual(first["celulas"]["A"], "01.00.01")

    def test_geojson_intactos(self):
        self.assertEqual(len(load_geojson("subprefeituras")["features"]), 32)
        self.assertEqual(len(load_geojson("mascara")["features"]), 1)
        self.assertEqual(len(load_geojson("metas")["features"]), 0)

    def test_mapa(self):
        f = geojson_meta("01")
        self.assertEqual(f["type"], "FeatureCollection")
        self.assertEqual(f["metadata"]["geometrias"], 9)
        self.assertEqual(f["metadata"]["poligonos_subprefeituras"], 13)

    def test_nada_publico_por_padrao(self):
        self.assertEqual(public_spreadsheet("01", released=False)["total_registros_publicos"], 0)
        one = public_spreadsheet("01", released=True)
        self.assertEqual(one["total_registros_publicos"], 23)
        for sheet in one["abas"]:
            for row in sheet["linhas"]:
                self.assertNotIn("Observações adicionais", row["campos"])
                if not row["localizacao_publicavel"]:
                    self.assertNotIn("Longitude", row["campos"])
                    self.assertNotIn("Latitude", row["campos"])
                    self.assertNotIn("Endereço", row["campos"])


if __name__ == "__main__":
    unittest.main()
