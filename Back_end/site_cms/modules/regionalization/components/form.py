import reflex as rx

from Back_end.site_cms.components.editor.common import (
    section_box,
    text_field,
    textarea_field,
)
from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


def regionalization_form() -> rx.Component:
    return rx.vstack(
        section_box(
            "Conteúdo",
            (
                "Textos que apresentam a regionalização "
                "das metas na Página Inicial."
            ),
            text_field(
                label="Título",
                value=SectionEditorState.regionalization_title,
                on_change=SectionEditorState.set_regionalization_title,
            ),
            text_field(
                label="Subtítulo",
                value=SectionEditorState.regionalization_subtitle,
                on_change=SectionEditorState.set_regionalization_subtitle,
            ),
            text_field(
                label="Instrução",
                value=SectionEditorState.regionalization_instruction,
                on_change=SectionEditorState.set_regionalization_instruction,
            ),
            textarea_field(
                label="Texto",
                value=SectionEditorState.regionalization_body,
                on_change=SectionEditorState.set_regionalization_body,
                min_height="220px",
            ),
        ),

        section_box(
            "Links",
            (
                "Recursos usados pelos botões da seção."
            ),
            text_field(
                label="Arquivo de regionalização",
                value=SectionEditorState.regionalization_document_url,
                on_change=SectionEditorState.set_regionalization_document_url,
            ),
            text_field(
                label="Dashboard",
                value=SectionEditorState.regionalization_dashboard_url,
                on_change=SectionEditorState.set_regionalization_dashboard_url,
            ),
        ),

        spacing="4",
        width="100%",
        align="stretch",
    )
