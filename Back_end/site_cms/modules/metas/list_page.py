"""Listagem de Metas com central de publicação e controle de origem em lote."""
import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.theme.semantic import BORDER, SURFACE, TEXT_PRIMARY, TEXT_SECONDARY
from Back_end.interface.theme.typography import FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY
from Back_end.site_cms.modules.metas.schema import FIELD_LABELS, META_FIELD_KEYS
from Back_end.site_cms.modules.metas.state import MetaCmsState as S


def _meta_row(meta) -> rx.Component:
    return rx.box(
        rx.grid(
            rx.hstack(
                rx.checkbox(
                    checked=meta["selected"],
                    on_change=lambda checked: S.bulk_toggle(meta["codigo"], checked),
                    size="2",
                ),
                rx.vstack(
                    rx.text("META", color="#1281AA", font_size="0.66rem", font_weight="700"),
                    rx.text(meta["codigo"], color=TEXT_PRIMARY,
                            font_family=FONT_FAMILY_SECUNDARY, font_size="1.25rem"),
                    spacing="1", align="start",
                ),
                align="center", spacing="3",
            ),
            rx.vstack(
                rx.text(meta["titulo"], font_weight="600", font_size="0.84rem", color=TEXT_PRIMARY),
                rx.text(meta["eixo"], font_size="0.72rem", color=TEXT_SECONDARY),
                rx.link("Abrir ficha", href=meta["url"], font_size="0.75rem"),
                align="start", spacing="1",
            ),
            rx.vstack(
                rx.badge(meta["status"], variant="soft", color_scheme=rx.cond(
                    meta["status"] == "Publicado", "green",
                    rx.cond(meta["status"] == "Não publicado", "gray", "orange"),
                )),
                rx.text("Campos publicados: ", meta["published_fields"], font_size="0.75rem", color=TEXT_SECONDARY),
                rx.text("Alterações pendentes: ", meta["pending_fields"], font_size="0.75rem", color=TEXT_SECONDARY),
                rx.text("Origens no rascunho: ", meta["cms_fields"], " CMS / ",
                        meta["smae_fields"], " SMAE", font_size="0.73rem", color=TEXT_SECONDARY),
                rx.cond(meta["conflitos"] != "0",
                        rx.badge(meta["conflitos"], " conflito(s) SMAE", color_scheme="red", variant="soft"),
                        rx.text("Sem conflitos", font_size="0.7rem", color=TEXT_SECONDARY)),
                align="start", spacing="1",
            ),
            rx.vstack(
                rx.badge(meta["field_status"], variant="soft", color_scheme=rx.cond(
                    meta["field_status"] == "Publicado", "green",
                    rx.cond(meta["field_status"] == "Pendente", "orange", "gray"),
                )),
                rx.text("Origem do rascunho: ", meta["field_source"], font_size="0.72rem"),
                rx.text("Origem publicada: ", meta["field_published_source"], font_size="0.72rem"),
                rx.text("SMAE disponível: ", meta["field_smae_available"],
                        font_size="0.72rem", color=TEXT_SECONDARY),
                rx.text("No site: ", meta["field_published_preview"],
                        font_size="0.72rem", color=TEXT_SECONDARY, word_break="break-word"),
                rx.text("No rascunho: ", meta["field_draft_preview"],
                        font_size="0.72rem", color=TEXT_SECONDARY, word_break="break-word"),
                align="start", spacing="1",
            ),
            columns={"initial": "1", "md": "2", "xl": "4"},
            spacing="4", align_items="start", width="100%",
        ),
        width="100%", padding="1rem", background=SURFACE,
        border=f"1px solid {BORDER}", border_radius="10px",
    )


def _bulk_toolbar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Central de publicação e origem", size="5", color=TEXT_PRIMARY),
                rx.text("Veja o que está no site, o que está em rascunho e qual fonte controla cada campo.",
                        color=TEXT_SECONDARY, font_size="0.82rem"),
                spacing="1", align="start",
            ),
            rx.spacer(),
            rx.button(rx.icon(tag="refresh_cw", size=14), "Recarregar",
                      on_click=S.load_metas, variant="outline", size="2"),
            width="100%", align="center", wrap="wrap", spacing="3",
        ),
        rx.hstack(
            rx.badge("Publicadas sem pendências: ", S.bulk_published_count,
                     color_scheme="green", size="2"),
            rx.badge("Rascunhos pendentes: ", S.bulk_pending_count,
                     color_scheme="orange", size="2"),
            rx.badge("Ainda não publicadas: ", S.bulk_unpublished_count,
                     color_scheme="gray", size="2"),
            rx.badge("Selecionadas: ", S.bulk_selected_count,
                     color_scheme="blue", size="2"),
            spacing="2", wrap="wrap",
        ),
        rx.hstack(
            rx.vstack(
                rx.text("Campo da ficha a verificar/gerenciar", font_weight="600", font_size="0.76rem"),
                rx.select.root(
                    rx.select.trigger(width="290px"),
                    rx.select.content(*[
                        rx.select.item(FIELD_LABELS[key], value=key) for key in META_FIELD_KEYS
                    ], position="popper"),
                    value=S.bulk_field, on_change=S.bulk_set_field,
                ),
                spacing="1", align="start",
            ),
            rx.vstack(
                rx.text("Situação da publicação", font_weight="600", font_size="0.76rem"),
                rx.select.root(
                    rx.select.trigger(width="220px"),
                    rx.select.content(
                        rx.select.item("Todas as metas", value="todos"),
                        rx.select.item("Publicado sem pendências", value="Publicado"),
                        rx.select.item("Rascunho pendente", value="Rascunho pendente"),
                        rx.select.item("Não publicado", value="Não publicado"),
                        position="popper",
                    ),
                    value=S.bulk_filter, on_change=S.bulk_set_filter,
                ),
                spacing="1", align="start",
            ),
            align="end", spacing="4", wrap="wrap", width="100%",
        ),
        rx.hstack(
            rx.button("Selecionar metas visíveis", on_click=S.bulk_select_visible,
                      variant="outline", size="2"),
            rx.button("Limpar seleção", on_click=S.bulk_clear_selection,
                      variant="ghost", size="2"),
            spacing="2", wrap="wrap",
        ),
        rx.cond(S.can_edit_content,
            rx.hstack(
                rx.button("Fixar campo no CMS", on_click=S.bulk_request("cms"),
                          color_scheme="blue", variant="soft", size="2"),
                rx.button("Voltar a usar SMAE", on_click=S.bulk_request("smae"),
                          color_scheme="orange", variant="soft", size="2"),
                spacing="2", wrap="wrap",
            ), rx.box(),
        ),
        rx.cond(S.can_publish_content,
            rx.hstack(
                rx.input(placeholder="Nota da publicação (opcional)",
                         value=S.bulk_publication_note,
                         on_change=S.bulk_set_publication_note,
                         width="330px", max_length=500),
                rx.button("Publicar rascunhos selecionados", on_click=S.bulk_request("publish"),
                          color_scheme="green", size="2"),
                spacing="2", wrap="wrap",
            ), rx.box(),
        ),
        rx.text(
            "Fixar no CMS mantém o valor atual, mas impede substituição automática pelo SMAE. "
            "Voltar ao SMAE copia o valor disponível para o rascunho. "
            "Nenhuma dessas ações altera o site até você publicar. "
            "Conflitos pendentes precisam de revisão antes da publicação em lote.",
            font_size="0.77rem", color=TEXT_SECONDARY,
        ),
        rx.cond(S.bulk_confirm_action != "",
            rx.vstack(
                rx.heading("Confirmar operação em lote", size="4", color=TEXT_PRIMARY),
                rx.text(S.bulk_action_label, " | ", S.bulk_confirm_count, " meta(s)"),
                rx.text("Campo selecionado: ", S.bulk_field_label,
                        font_size="0.82rem"),
                rx.text("A seleção foi congelada para esta confirmação. "
                        "Em caso de falha de validação, nenhuma meta será modificada.",
                        font_size="0.77rem", color=TEXT_SECONDARY),
                rx.hstack(
                    rx.button("Confirmar e aplicar", on_click=S.bulk_execute,
                              color_scheme="green", loading=S.bulk_working,
                              disabled=S.bulk_working),
                    rx.button("Cancelar", on_click=S.bulk_cancel,
                              variant="outline", disabled=S.bulk_working),
                    spacing="2",
                ),
                align="start", spacing="2", width="100%",
                padding="1rem", border="1px solid #A0AEC0", border_radius="10px",
            ), rx.box(),
        ),
        rx.cond(S.bulk_error != "", rx.callout(S.bulk_error, icon="triangle_alert",
                                               color_scheme="red", width="100%"), rx.box()),
        rx.cond(S.bulk_message != "", rx.callout(S.bulk_message, icon="check",
                                                 color_scheme="green", width="100%"), rx.box()),
        align="stretch", spacing="3", width="100%", padding="1.1rem",
        background=SURFACE, border=f"1px solid {BORDER}", border_radius="12px",
    )


def metas_cms_content() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text("SITE / METAS", color="#1281AA", font_size="0.72rem",
                        font_weight="700", letter_spacing="0.08em"),
                rx.heading("Fichas das Metas", size="7", color=TEXT_PRIMARY,
                           font_family=FONT_FAMILY_SECUNDARY),
                rx.text("Consulte, edite e publique o conteúdo das metas sem abrir cada ficha individualmente.",
                        color=TEXT_SECONDARY, font_family=FONT_FAMILY_PRIMARY, font_size="0.86rem"),
                spacing="2", align="start",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link(rx.button(rx.icon(tag="chart_no_axes_combined", size=14),
                                  "Visão Geral", background="#272361", color="white", cursor="pointer"),
                        href="/admin/site/metas/visao-geral", text_decoration="none"),
                rx.link(rx.button(rx.icon(tag="arrow_left", size=14), "Site", variant="outline",
                                  cursor="pointer"), href="/admin/site", text_decoration="none"),
                spacing="2", align="center",
            ),
            width="100%", align="start", wrap="wrap",
        ),
        _bulk_toolbar(),
        rx.input(placeholder="Buscar por número, título ou eixo...", value=S.search_text,
                 on_change=S.set_search_text, width="100%", max_width="520px"),
        rx.cond(S.list_error != "", rx.callout(S.list_error, icon="triangle_alert",
                                               color_scheme="red", width="100%"), rx.box()),
        rx.cond(S.list_loading,
                rx.center(rx.spinner(size="3"), width="100%", min_height="250px"),
                rx.vstack(
                    rx.text("Para cada meta, compare publicação, origem e valores do campo selecionado.",
                            color=TEXT_SECONDARY, font_size="0.75rem"),
                    rx.foreach(S.filtered_metas, _meta_row),
                    spacing="3", width="100%", align="stretch",
                ),
        ),
        spacing="5", width="100%", max_width="1350px", margin="0 auto",
        align="stretch", padding_bottom="5rem",
    )


def metas_cms_page() -> rx.Component:
    return admin_layout(metas_cms_content())
