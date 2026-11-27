"""Visualizacao administrativa de TODAS as abas e campos vinculados a uma Meta.

Nao consulta a tabela cms_meta_geo_records. A pagina usa o diretório data/
como fonte, e preserva edicoes editoriais existentes na ficha principal.
"""
from __future__ import annotations

import json
import reflex as rx

from Back_end.access.states.auth_state import AuthState
from Back_end.access.core.permissions import Permission
from Back_end.interface.layouts.admin_layout import admin_layout
from .fontes_leitor import all_sheets, audit, for_meta, meta_code
from .fontes_mapa import geojson_meta


class FontesMetaState(AuthState):
    codigo_fonte: str = ""
    abas_disponiveis: list[str] = []
    aba_selecionada: str = ""
    linhas_visiveis: list[dict[str, str]] = []
    limite: int = 20
    total_na_aba: int = 0
    total_meta: int = 0
    total_pontos: int = 0
    total_territorios: int = 0
    texto_erro: str = ""
    avisos: str = ""
    tipo_aba: str = ""
    carregando: bool = False

    def _recarregar(self):
        data = for_meta(self.codigo_fonte)
        self.total_meta = data["total_registros"]
        self.abas_disponiveis = [s["aba"] for s in data["abas"]]
        if self.aba_selecionada not in self.abas_disponiveis:
            self.aba_selecionada = self.abas_disponiveis[0] if self.abas_disponiveis else ""
        sheet = next((s for s in data["abas"] if s["aba"] == self.aba_selecionada), None)
        rows = (sheet or {}).get("linhas", [])
        if sheet and sheet.get("tipo") == "referencia_global":
            source = next((item for item in all_sheets() if item["aba"] == sheet["aba"]), None)
            rows = (source or {}).get("linhas", [])
            self.tipo_aba = "Referência compartilhada: não pertence a uma única meta"
        else:
            self.tipo_aba = "Registros associados à Meta " + self.codigo_fonte
        self.total_na_aba = len(rows)
        self.linhas_visiveis = [
            {
                "linha": str(r["linha"]),
                "arquivo": sheet["arquivo"],
                "json": json.dumps({"campos": r["campos"], "celulas_originais": r["celulas"],
                                    "formulas": r["formulas"], "vinculo": r.get("vinculo"),
                                    "tipo_linha": r.get("tipo")}, ensure_ascii=False, indent=2),
            }
            for r in rows[:self.limite]
        ]

    @rx.event
    def carregar(self):
        redirect = self._require_permission(Permission.SITE_VIEW)
        if redirect is not None:
            return redirect
        self.carregando = True
        self.texto_erro = ""
        yield
        try:
            # /admin/site/metas/01/mapa ou /territorio
            code = self.router.url.path.strip("/").split("/")[-2]
            self.codigo_fonte = meta_code(code) or ""
            if not self.codigo_fonte:
                raise ValueError("Codigo da Meta invalido")
            self.limite = 20
            self.aba_selecionada = ""
            self._recarregar()
            geo = geojson_meta(self.codigo_fonte)
            self.total_pontos = geo["metadata"]["geometrias"]
            self.total_territorios = geo["metadata"]["poligonos_subprefeituras"]
            report = audit()
            self.avisos = (f"Arquivos disponíveis: {len(report['fontes'])}. "
                           f"Abas encontradas na fonte atual: {report['total_abas']}. "
                           "Todas as colunas originais de cada linha estão preservadas.")
        except Exception as error:
            self.texto_erro = f"Falha na leitura das fontes: {error}"
            self.linhas_visiveis = []
        finally:
            self.carregando = False

    @rx.event
    def escolher_aba(self, value: str):
        redirect = self._require_permission(Permission.SITE_VIEW)
        if redirect is not None:
            return redirect
        self.aba_selecionada = value
        self.limite = 20
        self._recarregar()

    @rx.event
    def mais_linhas(self):
        redirect = self._require_permission(Permission.SITE_VIEW)
        if redirect is not None:
            return redirect
        self.limite += 20
        self._recarregar()


def _conteudo() -> rx.Component:
    return rx.vstack(
        rx.link(rx.button("Voltar para ficha", variant="outline"),
                href="/admin/site/metas/" + FontesMetaState.codigo_fonte),
        rx.link( rx.button( rx.icon("layers"), "Gerenciar camadas GEO", color_scheme="blue", variant="solid", cursor="pointer",),href="/admin/site/camadas-geo",),
        rx.heading("Mapa e arquivos da Meta " + FontesMetaState.codigo_fonte, size="6"),
        rx.text("Fontes originais da planilha e dos GeoJSON. Visualização administrativa, sem alterar o SMAE."),
        rx.cond(FontesMetaState.texto_erro != "", rx.text(FontesMetaState.texto_erro, color="red")),
        rx.text(FontesMetaState.avisos, color="gray"),
        rx.hstack(
            rx.badge("Linhas vinculadas: " + FontesMetaState.total_meta.to_string()),
            rx.badge("Geometrias: " + FontesMetaState.total_pontos.to_string()),
            rx.badge("Subprefeituras: " + FontesMetaState.total_territorios.to_string()),
            spacing="3", wrap="wrap",
        ),
        rx.heading("Informações por aba", size="4"),
        rx.cond(
            FontesMetaState.abas_disponiveis.length() > 0,
            rx.select(FontesMetaState.abas_disponiveis,
                      value=FontesMetaState.aba_selecionada,
                      on_change=FontesMetaState.escolher_aba,
                      width="100%"),
            rx.text("Nenhuma linha desta fonte foi associada à Meta. Verifique a aba e a coluna Meta do Excel."),
        ),
        rx.text(FontesMetaState.tipo_aba, color="gray"),
        rx.text("Linhas na aba selecionada: " + FontesMetaState.total_na_aba.to_string()),
        rx.foreach(
            FontesMetaState.linhas_visiveis,
            lambda row: rx.card(
                rx.vstack(
                    rx.text("Linha " + row["linha"] + " · " + row["arquivo"], weight="bold"),
                    rx.code_block(row["json"], language="json"),
                    align="stretch", spacing="2", width="100%",
                ),
                width="100%",
            ),
        ),
        rx.cond(FontesMetaState.linhas_visiveis.length() < FontesMetaState.total_na_aba,
                rx.button("Mostrar mais 20 linhas", on_click=FontesMetaState.mais_linhas, variant="outline")),
        spacing="4", width="100%", align="stretch", padding_bottom="5rem",
    )


def fontes_mapa_page() -> rx.Component:
    return admin_layout(_conteudo())
