"""Editor visual da ficha da Meta, inspirado no MetaModal.jsx do site.

Mantém o estado editorial existente, suas permissões, publicações e histórico.
Os campos de Regionalização 'planned' e 'executed' usam o Banco de Mídia.
"""
from __future__ import annotations

import reflex as rx

from Back_end.interface.theme.typography import FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY
from Back_end.site_cms.modules.metas.components.common import source_badge
from Back_end.site_cms.modules.metas.components.detail import (
    _action_row, action_bar, associated_projects_card, associated_works_card,
    classification_card, conflict_dialog, extra_sections_card, regionalization_card,
    meta_cms_breadcrumb, results_card,
)
from Back_end.site_cms.modules.metas.state import MetaCmsState

BORDER = "#E5E7EB"
MUTED = "#64748B"


def _section(title: str, *children, description: str = "") -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(title, font_family=FONT_FAMILY_SECUNDARY, font_size="2rem", font_weight="700", color=MetaCmsState.visual_axis_color, text_transform="uppercase"),
                rx.spacer(), width="100%", align="center"
            ),
            rx.cond(description != "", rx.text(description, color=MUTED, font_size="0.77rem"), rx.box()),
            *children, spacing="4", width="100%", align="stretch"
        ),
        width="100%", padding="1.3rem", background="white", border=f"1px solid {BORDER}",
        border_top=f"3px solid #E5E7EB", border_radius="16px",
    )


def _labelled(label: str, control, *, help_text: str = "") -> rx.Component:
    return rx.vstack(
        rx.text(label, font_size="0.76rem", font_weight="600", color="#374151"),
        control,
        rx.cond(help_text != "", rx.text(help_text, font_size="0.7rem", color=MUTED), rx.box()),
        width="100%", align="stretch", spacing="1"
    )


def _title_area() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.badge("META ", MetaCmsState.number, background=MetaCmsState.visual_axis_color, color="white", border_radius="50px", padding="0.4rem 1rem", font_size="1rem"),
            rx.badge(MetaCmsState.status_label, variant="soft", color_scheme=rx.cond(MetaCmsState.has_draft, "orange", "green")),
            rx.spacer(), source_badge(MetaCmsState.source_title), align="center", width="100%"
        ),
        rx.hstack(
            rx.heading(MetaCmsState.title_highlight, font_family=FONT_FAMILY_SECUNDARY, font_size={"initial": "2rem", "lg": "3.2rem"}, font_weight="700", color=MetaCmsState.visual_axis_color, text_transform="uppercase"),
            rx.heading(MetaCmsState.title_complement, font_family=FONT_FAMILY_SECUNDARY, font_size={"initial": "2rem", "lg": "3.2rem"}, font_weight="400", color=MetaCmsState.visual_axis_color, text_transform="uppercase"),
            spacing="3", width="100%", align="start", wrap="wrap"
        ),
        rx.cond(
            (MetaCmsState.title_highlight == "") & (MetaCmsState.title_complement == ""),
            rx.heading(MetaCmsState.title, color=MetaCmsState.visual_axis_color, font_family=FONT_FAMILY_SECUNDARY, font_size="2rem", text_transform="uppercase"),
            rx.box(),
        ),
        rx.grid(
            _labelled("Trecho destacado do título", rx.text_area(value=MetaCmsState.title_highlight, on_change=MetaCmsState.set_title_highlight, width="100%", min_height="65px")),
            _labelled("Complemento do título", rx.text_area(value=MetaCmsState.title_complement, on_change=MetaCmsState.set_title_complement, width="100%", min_height="65px")),
            columns={"initial": "1", "md": "2"}, spacing="3", width="100%"
        ),
        rx.button(
            rx.icon(tag="pencil", size=14),
            rx.cond(MetaCmsState.visual_show_title_fields, "Ocultar título original", "Editar título original e identificação"),
            on_click=MetaCmsState.toggle_visual_title_fields, variant="outline", size="2", width="100%"
        ),
        rx.cond(MetaCmsState.visual_show_title_fields,
            rx.vstack(
                _labelled("Título completo", rx.text_area(value=MetaCmsState.title, on_change=MetaCmsState.set_title, min_height="90px", width="100%")),
                rx.grid(
                    _labelled("Número", rx.input(value=MetaCmsState.number, on_change=MetaCmsState.set_number, width="100%")),
                    _labelled("Eixo", rx.input(value=MetaCmsState.axis_name, on_change=MetaCmsState.set_axis_name, width="100%")),
                    columns={"initial": "1", "md": "2"}, spacing="3", width="100%"
                ),
                width="100%", align="stretch", spacing="3"
            ), rx.box()
        ),
        width="100%", align="stretch", spacing="4", padding="1rem 1.3rem", background="white",
        border_radius="16px", font_family=FONT_FAMILY_PRIMARY,
    )


def _projection_agency() -> rx.Component:
    return _section(
        "Projeção e órgão",
        rx.vstack(
            rx.text("PROJEÇÃO", color=MetaCmsState.visual_axis_color, font_family=FONT_FAMILY_SECUNDARY, font_size="1.55rem"),
            rx.text(MetaCmsState.projection, color="#1F2937", white_space="pre-wrap", font_size="0.89rem"),
            rx.text_area(value=MetaCmsState.projection, on_change=MetaCmsState.set_projection, width="100%", min_height="100px", placeholder="Texto da projeção da Meta"),
            rx.divider(color=MetaCmsState.visual_axis_color),
            rx.text("ÓRGÃO", color=MetaCmsState.visual_axis_color, font_family=FONT_FAMILY_SECUNDARY, font_size="1.55rem"),
            rx.heading(MetaCmsState.responsible_agencies_text, color=MetaCmsState.visual_axis_color, font_family=FONT_FAMILY_SECUNDARY, font_size="1.7rem"),
            _labelled("Siglas dos órgãos, uma por linha", rx.text_area(value=MetaCmsState.responsible_agencies_text, on_change=MetaCmsState.set_responsible_agencies_text, width="100%", min_height="65px")),
            spacing="3", width="100%", align="stretch"
        ),
    )


def _action_visual(item, index) -> rx.Component:
    return rx.box(
        rx.button(
            rx.hstack(
                rx.text(item["number"], " · ", item["description"], flex="1", text_align="left", white_space="normal", color="#1F2937", font_weight="600", font_size="0.88rem"),
                rx.cond(item["completed"] == "true", rx.icon(tag="circle_check", color=MetaCmsState.visual_axis_color, size=18), rx.box()),
                rx.icon(tag="chevron_down", color=MetaCmsState.visual_axis_color, size=17),
                width="100%", align="center", spacing="2"
            ),
            on_click=MetaCmsState.toggle_visual_action(index), background="#F8FAFC", color="#111827", width="100%", height="auto",
            padding="1rem", border_radius="0", text_align="left", cursor="pointer"
        ),
        rx.cond(
            MetaCmsState.visual_open_action_index == index,
            rx.box(_action_row(item, index), padding="0.6rem 0.9rem", background="white"),
            rx.box(),
        ),
        border_bottom=f"1px solid {BORDER}", width="100%", overflow="hidden"
    )


def _actions() -> rx.Component:
    return _section(
        "Ações estratégicas",
        rx.hstack(
            rx.text("✓ Ação concluída", color=MetaCmsState.visual_axis_color, font_size="0.74rem"),
            rx.spacer(),
            rx.button(rx.icon(tag="plus", size=14), "Adicionar ação", size="2", variant="outline", on_click=MetaCmsState.add_action),
            width="100%", align="center"
        ),
        rx.box(
            rx.foreach(MetaCmsState.strategic_actions, _action_visual),
            width="100%", border=f"1px solid {BORDER}", border_radius="12px", overflow="hidden", background="#F8FAFC"
        ),
        description="Clique em uma ação para alterar descrição, conclusão e evolução."
    )


def _region_image_preview() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text("PLANEJADA", font_weight="700", font_size="0.75rem", color="white"),
            rx.switch(checked=MetaCmsState.visual_region_tab == "executed", on_change=MetaCmsState.set_visual_region_executed, color_scheme="gray"),
            rx.text("EXECUTADA", font_weight="700", font_size="0.75rem", color="white"),
            width="fit-content", align="center", spacing="3", background=MetaCmsState.visual_axis_color,
            border_radius="12px 12px 0 0", padding="0.8rem 1rem"
        ),
        rx.box(
            rx.cond(
                MetaCmsState.visual_active_image != "",
                rx.image(src=MetaCmsState.visual_active_image, width="100%", height="auto", max_height="460px", object_fit="contain", background="#F8FAFC"),
                rx.center(
                    rx.vstack(rx.icon(tag="image", color="#94A3B8", size=34), rx.text("Imagem não cadastrada", color=MUTED), align="center"),
                    width="100%", min_height="240px", background="#F8FAFC"
                ),
            ),
            width="100%", border_radius="0 14px 14px 14px", border=f"1px solid {BORDER}", overflow="hidden",
        ),
        rx.cond(MetaCmsState.visual_active_text != "", rx.text(MetaCmsState.visual_active_text, font_size="0.82rem", color="#374151", white_space="pre-wrap"), rx.box()),
        rx.cond(MetaCmsState.visual_active_footer != "", rx.text(MetaCmsState.visual_active_footer, font_size="0.75rem", color=MUTED, text_align="center", text_decoration="underline"), rx.box()),
        spacing="2", width="100%", align="stretch"
    )


def _media_option(asset, slot: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.image(src=asset["url"], width="100%", height="75px", object_fit="contain", background="#F8FAFC"),
            rx.text(asset["name"], font_size="0.68rem", overflow="hidden", text_overflow="ellipsis", white_space="nowrap", width="100%"),
            rx.button("Selecionar", on_click=MetaCmsState.choose_region_media(slot, asset["id"]), width="100%", size="1", variant="soft", cursor="pointer"),
            spacing="2", width="100%", align="stretch"
        ), padding="0.55rem", border=f"1px solid {BORDER}", border_radius="10px", width="100%"
    )


def _region_media_browser(slot: str) -> rx.Component:
    return rx.cond(
        MetaCmsState.visual_media_picker == slot,
        rx.box(
            rx.vstack(
                rx.text("Escolher imagem do Banco de Mídia", font_size="0.78rem", font_weight="600"),
                rx.cond(MetaCmsState.visual_media_count > 0,
                    rx.grid(rx.foreach(MetaCmsState.visual_media_assets, lambda asset: _media_option(asset, slot)), columns={"initial": "2", "md": "3", "xl": "4"}, spacing="2", width="100%"),
                    rx.text("Nenhuma imagem cadastrada. Use o envio abaixo ou abra o Banco de Mídia.", font_size="0.78rem", color=MUTED)
                ),
                rx.button("Fechar seleção", on_click=MetaCmsState.toggle_region_media_picker(slot), variant="outline", size="1"),
                spacing="3", align="stretch", width="100%"
            ), padding="0.8rem", background="#F8FAFC", border_radius="10px", width="100%"
        ),
        rx.box()
    )


def _region_upload(slot: str) -> rx.Component:
    upload_id = f"meta_cms_regionalizacao_{slot}"
    uploader = MetaCmsState.upload_region_planned if slot == "planned" else MetaCmsState.upload_region_executed
    return rx.vstack(
        rx.upload(
            rx.hstack(rx.icon(tag="cloud_upload", color=MUTED, size=19), rx.text("Clique ou arraste a imagem (PNG, JPG, SVG)", font_size="0.73rem", color=MUTED), spacing="2", align="center"),
            id=upload_id, multiple=False, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"], "image/svg+xml": [".svg"]},
            width="100%", padding="0.7rem", border="1px dashed #94A3B8", border_radius="10px"
        ),
        rx.button("Enviar e usar imagem", on_click=uploader(rx.upload_files(upload_id=upload_id)), size="2", variant="outline", disabled=MetaCmsState.visual_media_uploading, cursor="pointer"),
        width="100%", align="stretch", spacing="2"
    )


def _region_slot_editor(item, index) -> rx.Component:
    slot = item["key"]
    return rx.cond(
        (slot == "planned") | (slot == "executed"),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading(rx.cond(slot == "planned", "Imagem planejada", "Imagem executada"), size="4", color=MetaCmsState.visual_axis_color),
                    rx.spacer(),
                    rx.badge(rx.cond(item["enabled"] == "true", "Visível", "Oculta"), color_scheme=rx.cond(item["enabled"] == "true", "green", "gray")),
                    width="100%", align="center"
                ),
                rx.cond(item["image_preview"] != "", rx.image(src=item["image_preview"], width="100%", max_height="230px", object_fit="contain", background="#F8FAFC", border_radius="10px"), rx.box()),
                rx.hstack(
                    rx.button("Buscar no Banco de Mídia", on_click=MetaCmsState.toggle_region_media_picker(slot), variant="soft", size="2", cursor="pointer"),
                    rx.link(rx.button("Abrir biblioteca", variant="outline", size="2"), href="/admin/midias", text_decoration="none", is_external=True),
                    spacing="2", wrap="wrap", width="100%"
                ),
                rx.cond(slot == "planned", _region_media_browser("planned"), _region_media_browser("executed")),
                rx.cond(slot == "planned", _region_upload("planned"), _region_upload("executed")),
                _labelled("URL ou referência atual", rx.input(value=item["image_url"], on_change=lambda v: MetaCmsState.update_region_block_field(index, "image_url", v), width="100%", placeholder="Imagem antiga ou media:123"), help_text="Você pode substituir pela biblioteca ou manter a imagem anterior."),
                _labelled("Texto opcional abaixo da imagem", rx.text_area(value=item["text"], on_change=lambda v: MetaCmsState.update_region_block_field(index, "text", v), width="100%", min_height="65px", placeholder="Deixe vazio para não mostrar texto")),
                _labelled("Legenda opcional", rx.text_area(value=item["footer"], on_change=lambda v: MetaCmsState.update_region_block_field(index, "footer", v), width="100%", min_height="65px", placeholder="Deixe vazio para não mostrar legenda")),
                rx.hstack(
                    rx.text("Exibir bloco", font_size="0.75rem", color=MUTED),
                    rx.select.root(rx.select.trigger(width="140px"), rx.select.content(rx.select.item("Sim", value="true"), rx.select.item("Não", value="false"), position="popper"), value=item["enabled"], on_change=lambda v: MetaCmsState.update_region_block_field(index, "enabled", v)),
                    width="100%", align="center"
                ),
                spacing="3", width="100%", align="stretch"
            ), padding="1rem", border=f"1px solid {BORDER}", border_radius="12px", background="white", width="100%"
        ),
        rx.box()
    )


def _regionalization() -> rx.Component:
    return _section(
        "Regionalização",
        rx.text("Prévia: alterne entre Planejada e Executada como no site público.", color=MUTED, font_size="0.76rem"),
        _region_image_preview(),
        rx.grid(
            _labelled("Tipo de regionalização", rx.select.root(
                rx.select.trigger(width="100%"),
                rx.select.content(rx.select.item("Não regionalizável", value="not_regionalizable"), rx.select.item("Personalizada (imagens)", value="custom"), position="popper"),
                value=MetaCmsState.regionalization_mode, on_change=MetaCmsState.set_regionalization_mode,
            )),
            _labelled("Nota opcional da regionalização", rx.text_area(value=MetaCmsState.regionalization_note, on_change=MetaCmsState.set_regionalization_note, min_height="60px", width="100%")),
            columns={"initial": "1", "md": "2"}, spacing="3", width="100%"
        ),
        rx.callout("As imagens são guardadas como rascunho até clicar em Salvar. Só aparecem no site após Publicar.", icon="info", color_scheme="blue", size="1"),
        rx.vstack(rx.foreach(MetaCmsState.regionalization_blocks, _region_slot_editor), width="100%", align="stretch", spacing="3"),
        rx.cond(MetaCmsState.visual_media_message != "", rx.text(MetaCmsState.visual_media_message, color=MetaCmsState.visual_axis_color, font_size="0.8rem"), rx.box()),
        description="Duas imagens independentes. Textos e legendas são opcionais."
    )


def _monitoring_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Monitoramento", font_family=FONT_FAMILY_SECUNDARY, color=MetaCmsState.visual_axis_color, font_size="2rem", text_transform="uppercase"),
            rx.hstack(
                rx.badge("Em planejamento", background=rx.cond(MetaCmsState.monitoring == "planejamento", MetaCmsState.visual_axis_color, "#E5E7EB"), color=rx.cond(MetaCmsState.monitoring == "planejamento", "white", MUTED)),
                rx.badge("Em progresso", background=rx.cond(MetaCmsState.monitoring == "progresso", MetaCmsState.visual_axis_color, "#E5E7EB"), color=rx.cond(MetaCmsState.monitoring == "progresso", "white", MUTED)),
                rx.badge("Atingida", background=rx.cond(MetaCmsState.monitoring == "atingida", MetaCmsState.visual_axis_color, "#E5E7EB"), color=rx.cond(MetaCmsState.monitoring == "atingida", "white", MUTED)),
                width="100%", spacing="1", wrap="wrap"
            ),
            _labelled("Situação da Meta", rx.select.root(
                rx.select.trigger(width="100%"),
                rx.select.content(rx.select.item("Em planejamento", value="planejamento"), rx.select.item("Em progresso", value="progresso"), rx.select.item("Atingida", value="atingida"), position="popper"),
                value=MetaCmsState.monitoring, on_change=MetaCmsState.set_monitoring,
            )),
            rx.divider(color=MetaCmsState.visual_axis_color),
            rx.heading("Resultados apurados", font_family=FONT_FAMILY_SECUNDARY, color=MetaCmsState.visual_axis_color, font_size="1.7rem"),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.cond(MetaCmsState.visual_has_many_results, rx.button(rx.icon(tag="chevron_left", size=15), variant="ghost", size="1", on_click=MetaCmsState.visual_previous_result), rx.box()),
                        rx.text(MetaCmsState.visual_result_period, color=MetaCmsState.visual_axis_color, font_size="0.75rem", font_weight="700"),
                        rx.cond(MetaCmsState.visual_has_many_results, rx.button(rx.icon(tag="chevron_right", size=15), variant="ghost", size="1", on_click=MetaCmsState.visual_next_result), rx.box()),
                        width="100%", justify="between", align="center"
                    ),
                    rx.heading(MetaCmsState.visual_result_value, color="white", background=MetaCmsState.visual_axis_color, padding="1rem", width="100%", text_align="center"),
                    spacing="0", align="center", width="100%"
                ), border=f"1px solid {BORDER}", border_radius="10px", overflow="hidden", width="100%"
            ),
            results_card(),
            rx.divider(color=MetaCmsState.visual_axis_color),
            rx.heading("Indicador", font_family=FONT_FAMILY_SECUNDARY, color=MetaCmsState.visual_axis_color, font_size="1.7rem"),
            rx.text(MetaCmsState.indicator, font_size="0.83rem", color="#334155"),
            rx.text_area(value=MetaCmsState.indicator, on_change=MetaCmsState.set_indicator, width="100%", min_height="85px"),
            rx.divider(color=MetaCmsState.visual_axis_color),
            rx.heading("Evolução da Meta", font_family=FONT_FAMILY_SECUNDARY, color=MetaCmsState.visual_axis_color, font_size="1.7rem"),
            rx.text_area(value=MetaCmsState.evolution, on_change=MetaCmsState.set_evolution, min_height="200px", width="100%"),
            spacing="4", width="100%", align="stretch"
        ),
        border_radius="16px", padding="1.2rem", background="white", border=f"1px solid {BORDER}",
        box_shadow="0 10px 30px rgba(0,0,0,0.08)", width="100%",
    )


def _footer() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.box(rx.heading(MetaCmsState.axis_name, color="white", font_size="2rem", font_family=FONT_FAMILY_SECUNDARY), background=MetaCmsState.visual_axis_secondary, padding="1.1rem", border_radius="12px", min_width="190px"),
            rx.vstack(
                rx.heading(MetaCmsState.visual_axis_phrase_one, font_size="1.3rem", font_weight="700", color="white"),
                rx.text(MetaCmsState.visual_axis_phrase_two, font_size="0.95rem", color="white"),
                align="stretch", spacing="3", flex="1"
            ),
            direction={"initial": "column", "lg": "row"}, gap="5", align="center", width="100%"
        ),
        background=MetaCmsState.visual_axis_color, width="100%", border_radius="16px", padding="1.5rem"
    )


def _advanced() -> rx.Component:
    return rx.box(
        rx.button(
            rx.icon(tag="settings_2", size=16),
            rx.cond(MetaCmsState.visual_show_advanced, "Ocultar outros campos da Meta", "Editar campos complementares"),
            on_click=MetaCmsState.toggle_visual_advanced, variant="outline", width="100%", cursor="pointer"
        ),
        rx.cond(
            MetaCmsState.visual_show_advanced,
            rx.vstack(
                classification_card(),
                regionalization_card(),
                associated_works_card(),
                associated_projects_card(),
                extra_sections_card(),
                spacing="4", width="100%", align="stretch"
            ),
            rx.box()
        ), width="100%"
    )


def visual_meta_editor() -> rx.Component:
    """Ficha de edição com a hierarquia visual do layout React de referência."""
    return rx.vstack(
        meta_cms_breadcrumb(),
        rx.box(
            rx.hstack(
                rx.link(rx.button(rx.icon(tag="arrow_left", size=15), "Voltar", color="white", variant="ghost"), href="/admin/site/metas", text_decoration="none"),
                rx.spacer(),
                rx.button(rx.icon(tag="save", size=14), "Salvar rascunho", on_click=MetaCmsState.save_draft, variant="soft", disabled=~MetaCmsState.can_edit_content),
                rx.cond(MetaCmsState.can_publish_content, rx.button("Publicar", on_click=MetaCmsState.publish, variant="solid", background="#272361", color="white"), rx.box()),
                align="center", width="100%", spacing="2", wrap="wrap"
            ), background=MetaCmsState.visual_axis_color, padding="0.8rem 1rem", width="100%", border_radius="12px"
        ),
        _title_area(),
        rx.flex(
            rx.vstack(_projection_agency(), _actions(), _regionalization(), spacing="4", width={"initial": "100%", "xl": "0"}, flex={"initial": "none", "xl": "2"}, min_width="0", align="stretch"),
            rx.box(_monitoring_panel(), width={"initial": "100%", "xl": "0"}, flex={"initial": "none", "xl": "1"}, min_width="0", position={"initial": "static", "xl": "sticky"}, top="1rem"),
            direction={"initial": "column", "xl": "row"}, gap="4", align="start", width="100%"
        ),
        _footer(),
        _advanced(),
        rx.link(rx.button("Abrir Mapa e fontes das 13 abas", variant="outline", width="100%"), href="/admin/site/metas/" + MetaCmsState.meta_code + "/mapa", text_decoration="none", width="100%"),
        action_bar(),
        conflict_dialog(),
        spacing="4", width="100%", align="stretch", min_width="0", padding_bottom="1rem", font_family=FONT_FAMILY_PRIMARY
    )
