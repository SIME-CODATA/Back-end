import reflex as rx

from Back_end.site_cms.components.editor.common import (
    media_notice,
    section_box,
    text_field,
    textarea_field,
)
from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


def about_form() -> rx.Component:
    return rx.vstack(
        section_box(
            "Apresentação",
            (
                "Campos que hoje acompanham a seção da carta "
                "no site antigo."
            ),
            text_field(
                label="Título",
                value=SectionEditorState.about_title,
                on_change=SectionEditorState.set_about_title,
            ),
            text_field(
                label="Subtítulo",
                value=SectionEditorState.about_subtitle,
                on_change=SectionEditorState.set_about_subtitle,
            ),
            textarea_field(
                label="Texto de apresentação",
                value=SectionEditorState.about_body,
                on_change=SectionEditorState.set_about_body,
                min_height="150px",
            ),
        ),

        section_box(
            "Carta do prefeito",
            (
                "Conteúdo institucional exibido como palavra "
                "ou carta do prefeito."
            ),
            text_field(
                label="Título da carta",
                value=SectionEditorState.letter_title,
                on_change=SectionEditorState.set_letter_title,
            ),
            text_field(
                label="Nome do prefeito",
                value=SectionEditorState.letter_author,
                on_change=SectionEditorState.set_letter_author,
            ),
            textarea_field(
                label="Parágrafos",
                value=SectionEditorState.letter_paragraphs_text,
                on_change=SectionEditorState.set_letter_paragraphs_text,
                help_text=(
                    "Separe os parágrafos deixando uma linha em branco."
                ),
                min_height="360px",
            ),
        ),

        section_box(
            "Recursos",
            (
                "Referências atuais de imagem e documento. "
                "O upload será integrado ao banco de imagens depois."
            ),
            media_notice(),
            text_field(
                label="Imagem atual",
                value=SectionEditorState.about_image_url,
                on_change=SectionEditorState.set_about_image_url,
                help_text="Referência temporária do conteúdo legado.",
            ),
            text_field(
                label="Documento / PDF",
                value=SectionEditorState.about_pdf_url,
                on_change=SectionEditorState.set_about_pdf_url,
            ),
        ),

        spacing="4",
        width="100%",
        align="stretch",
    )
