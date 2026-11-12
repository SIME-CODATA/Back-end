"""Tela de geografia vinculada à edição individual da Meta."""
import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.site_cms.modules.metas.geografia.state import GeoCmsState


def _row_item(item) -> rx.Component:
    return rx.button(
        rx.vstack(
            rx.hstack(
                rx.text(item["codigo"], weight="bold"),
                rx.spacer(),
                rx.badge(item["status"], variant="soft"),
                width="100%",
            ),
            rx.text(item["descricao"], size="2", text_align="left"),
            rx.text("Distrito: ", item["distrito"], size="1"),
            rx.text("Publicável na origem: ", item["publicavel"], size="1"),
            rx.text("Conflitos: ", item["conflitos"], size="1"),
            width="100%", align="start", spacing="1",
        ),
        on_click=GeoCmsState.select_record(item["id"]),
        width="100%", height="auto", padding="12px", variant="outline",
        white_space="normal", text_align="left",
    )


def _field_item(item) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(item["label"], font_weight="600", font_size="0.85rem"),
            rx.badge(item["source"], variant="soft"),
            rx.cond(item["conflict"] == "sim", rx.badge("Atualização em conflito", color_scheme="orange"), rx.box()),
            rx.spacer(),
            rx.cond((item["locked"] == "nao") & (item["has_source"] == "sim"), rx.button(
                "Usar valor de origem", size="1", variant="ghost",
                on_click=GeoCmsState.restore_field(item["key"]),
            ), rx.box()),
            width="100%", align="center", wrap="wrap",
        ),
        rx.text_area(
            value=item["value"],
            on_change=lambda val: GeoCmsState.edit_field(item["key"], val),
            width="100%", min_height="62px", resize="vertical",
            disabled=item["locked"] == "sim",
        ),
        rx.cond(item["source"] == "manual", rx.text("Valor da fonte: ", item["original"], font_size="0.71rem", color="gray"), rx.box()),
        align="stretch", width="100%", spacing="2",
        padding="12px", border="1px solid #D7DEE7", border_radius="9px",
    )


def geo_cms_page() -> rx.Component:
    return admin_layout(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Monitoramento territorial", size="6"),
                    rx.text("Meta ", GeoCmsState.meta_code,
                            " · Dados completos da planilha, sem sobrescrever o SMAE ou as fichas existentes.",
                            color="gray", size="2"),
                    align="start", spacing="1",
                ),
                rx.spacer(),
                rx.button("Novo registro manual", on_click=GeoCmsState.create_record, color_scheme="blue"),
                align="center", width="100%", wrap="wrap",
            ),
            rx.cond(GeoCmsState.error_geo != "", rx.callout(GeoCmsState.error_geo, color_scheme="red"), rx.box()),
            rx.cond(GeoCmsState.notice_geo != "", rx.callout(GeoCmsState.notice_geo, color_scheme="green"), rx.box()),
            rx.hstack(
                rx.upload(
                    rx.text("Selecionar CSV, Excel ou JSON", font_weight="600", font_size="0.84rem"),
                    id="geo_import_file", max_files=1, multiple=False,
                    accept={
                        "text/csv": [".csv"],
                        "application/json": [".json"],
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
                        "application/vnd.ms-excel.sheet.macroEnabled.12": [".xlsm"],
                    },
                    padding="12px", border="1px dashed #64748b", border_radius="9px",
                ),
                rx.button("Importar arquivo para rascunho",
                          on_click=GeoCmsState.upload_geography(rx.upload_files(upload_id="geo_import_file")),
                          variant="outline"),
                rx.text("O arquivo pode incluir registros de todas as 132 metas. Nenhuma linha é publicada automaticamente.",
                        font_size="0.76rem", color="gray"),
                wrap="wrap", align="center", width="100%",
            ),
            rx.callout("Campos 'Meta' e 'codigo' são identificadores fixos. Notas internas, "
                       "geometrias não aprovadas e localizações marcadas como não publicáveis "
                       "não saem na API pública.", color_scheme="blue"),
            rx.cond(GeoCmsState.loading, rx.spinner(), rx.grid(
                rx.vstack(
                    rx.text("Registros encontrados: ", GeoCmsState.total_registros, font_weight="600"),
                    rx.box(rx.vstack(rx.foreach(GeoCmsState.rows, _row_item), spacing="2", width="100%"),
                           max_height="72vh", overflow_y="auto", width="100%"),
                    align="stretch", width="100%",
                ),
                rx.vstack(
                    rx.cond(GeoCmsState.selected_id > 0,
                        rx.vstack(
                            rx.hstack(
                                rx.text("Origem: ", GeoCmsState.selected_source),
                                rx.badge(GeoCmsState.selected_status),
                                rx.text("Conflitos: ", GeoCmsState.pending_count),
                                width="100%", wrap="wrap",
                            ),
                            rx.hstack(
                                rx.button("Salvar rascunho", on_click=GeoCmsState.save_changes, variant="outline"),
                                rx.cond(GeoCmsState.can_publish_geo,
                                    rx.hstack(
                                        rx.button("Publicar", on_click=GeoCmsState.publish_record, color_scheme="green"),
                                        rx.button("Retirar publicação", on_click=GeoCmsState.unpublish_record,
                                                  color_scheme="red", variant="soft"),
                                    ), rx.box()),
                                wrap="wrap",
                            ),
                            rx.box(rx.vstack(rx.foreach(GeoCmsState.fields, _field_item), spacing="3", width="100%"),
                                   max_height="70vh", overflow_y="auto", width="100%"),
                            align="stretch", width="100%", spacing="3",
                        ),
                        rx.text("Selecione um registro à esquerda para visualizar e editar todas as 19 colunas.",
                                color="gray"),
                    ),
                    width="100%", align="stretch",
                ),
                columns={"initial": "1", "lg": "2"}, spacing="4", width="100%", align_items="start",
            )),
            width="100%", align="stretch", spacing="4", padding_bottom="5rem",
        )
    )
