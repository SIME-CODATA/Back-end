import reflex as rx

from Back_end.site_cms.components.editor.common import (CARD_BG,CARD_BORDER,TEXT_PRIMARY,media_notice,section_box,text_field,textarea_field,)
from Back_end.site_cms.state.section_editor_state import (SectionEditorState,)


def _how_card(item, index) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Etapa ",
                    index + 1,
                    color=TEXT_PRIMARY,
                    font_size="0.82rem",
                    font_weight="700",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(
                        tag="trash_2",
                        size=14,
                    ),
                    "Remover",
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=lambda: (
                        SectionEditorState.remove_site_about_how_card(
                            index
                        )
                    ),
                ),
                width="100%",
                align="center",
            ),

            rx.grid(
                text_field(
                    label="Número",
                    value=item["number"],
                    on_change=lambda value: (
                        SectionEditorState.update_site_about_how_number(
                            index,
                            value,
                        )
                    ),
                ),
                text_field(
                    label="Título",
                    value=item["title"],
                    on_change=lambda value: (
                        SectionEditorState.update_site_about_how_title(
                            index,
                            value,
                        )
                    ),
                ),
                columns={
                    "initial": "1",
                    "md": "2",
                },
                spacing="3",
                width="100%",
            ),

            textarea_field(
                label="Conteúdo",
                value=item["content"],
                on_change=lambda value: (
                    SectionEditorState.update_site_about_how_content(
                        index,
                        value,
                    )
                ),
                min_height="130px",
            ),

            textarea_field(
                label="Detalhe",
                value=item["detail"],
                on_change=lambda value: (
                    SectionEditorState.update_site_about_how_detail(
                        index,
                        value,
                    )
                ),
                min_height="100px",
            ),

            spacing="3",
            width="100%",
            align="stretch",
        ),
        width="100%",
        padding="1rem",
        background=CARD_BG,
        border=f"1px solid {CARD_BORDER}",
        border_radius="10px",
    )


def about_page_form() -> rx.Component:
    return rx.vstack(
        section_box(
            "Banner",
            "Apresentação principal da página Sobre o PdM.",
            text_field(
                label="Supertítulo",
                value=SectionEditorState.site_about_eyebrow,
                on_change=SectionEditorState.set_site_about_eyebrow,
            ),
            text_field(
                label="Título",
                value=SectionEditorState.site_about_title,
                on_change=SectionEditorState.set_site_about_title,
            ),
            text_field(
                label="Subtítulo",
                value=SectionEditorState.site_about_subtitle,
                on_change=SectionEditorState.set_site_about_subtitle,
            ),
            media_notice(),
            text_field(
                label="Documento principal (primeiro botão)",
                value=SectionEditorState.site_about_pdf_url,
                on_change=SectionEditorState.set_site_about_pdf_url,
            ),
            text_field(
                label="Documento complementar (segundo botão)",
                value=SectionEditorState.site_about_pdf2_url,
                on_change=SectionEditorState.set_site_about_pdf2_url,
            ),
        ),

        section_box(
            "O que, por que e para quem",
            "Textos resumidos de apresentação do Programa de Metas.",
            textarea_field(
                label="O que é",
                value=SectionEditorState.site_about_what,
                on_change=SectionEditorState.set_site_about_what,
                min_height="130px",
            ),
            textarea_field(
                label="Por que existe",
                value=SectionEditorState.site_about_why,
                on_change=SectionEditorState.set_site_about_why,
                min_height="130px",
            ),
            textarea_field(
                label="Para quem",
                value=SectionEditorState.site_about_for_whom,
                on_change=SectionEditorState.set_site_about_for_whom,
                min_height="130px",
            ),
        ),

        section_box(
            "Objetivos",
            "Objetivos institucionais apresentados na página.",
            textarea_field(
                label="Transparência",
                value=SectionEditorState.site_about_objective_transparency,
                on_change=SectionEditorState.set_site_about_objective_transparency,
            ),
            textarea_field(
                label="Visão sistêmica",
                value=SectionEditorState.site_about_objective_systemic_view,
                on_change=SectionEditorState.set_site_about_objective_systemic_view,
            ),
            textarea_field(
                label="Otimização",
                value=SectionEditorState.site_about_objective_optimization,
                on_change=SectionEditorState.set_site_about_objective_optimization,
            ),
            textarea_field(
                label="Execução",
                value=SectionEditorState.site_about_objective_execution,
                on_change=SectionEditorState.set_site_about_objective_execution,
            ),
        ),

        section_box(
            "Como foi feito",
            "Texto geral e etapas do processo de construção do PdM.",
            textarea_field(
                label="Texto",
                value=SectionEditorState.site_about_how_text,
                on_change=SectionEditorState.set_site_about_how_text,
                min_height="180px",
            ),
            rx.hstack(
                rx.spacer(),
                rx.button(
                    rx.icon(
                        tag="plus",
                        size=14,
                    ),
                    "Adicionar etapa",
                    size="2",
                    variant="soft",
                    on_click=SectionEditorState.add_site_about_how_card,
                ),
                width="100%",
            ),
            rx.vstack(
                rx.foreach(
                    SectionEditorState.site_about_how_cards,
                    _how_card,
                ),
                spacing="3",
                width="100%",
                align="stretch",
            ),
        ),

        section_box(
            "Indicadores",
            "Textos institucionais da área de indicadores.",
            textarea_field(
                label="Texto",
                value=SectionEditorState.site_about_indicators_text,
                on_change=SectionEditorState.set_site_about_indicators_text,
            ),
            text_field(
                label="Subtítulo",
                value=SectionEditorState.site_about_indicators_subtitle,
                on_change=SectionEditorState.set_site_about_indicators_subtitle,
            ),
            text_field(
                label="Chamada da subseção",
                value=SectionEditorState.site_about_indicators_section_call,
                on_change=SectionEditorState.set_site_about_indicators_section_call,
            ),
            textarea_field(
                label="Conteúdo da subseção",
                value=SectionEditorState.site_about_indicators_section_content,
                on_change=SectionEditorState.set_site_about_indicators_section_content,
                min_height="160px",
            ),
        ),

        section_box(
            "Participação",
            (
                "Textos de participação que pertencem à página Sobre. "
                "A página específica de Participação Social será tratada "
                "separadamente depois."
            ),
            textarea_field(
                label="Texto",
                value=SectionEditorState.site_about_participation_text,
                on_change=SectionEditorState.set_site_about_participation_text,
            ),
            textarea_field(
                label="Audiências",
                value=SectionEditorState.site_about_hearings_content,
                on_change=SectionEditorState.set_site_about_hearings_content,
                min_height="160px",
            ),
            text_field(
                label="Vídeo de audiências",
                value=SectionEditorState.site_about_hearings_video_url,
                on_change=SectionEditorState.set_site_about_hearings_video_url,
            ),
            textarea_field(
                label="Devolutivas",
                value=SectionEditorState.site_about_feedback_content,
                on_change=SectionEditorState.set_site_about_feedback_content,
                min_height="160px",
            ),
        ),

        spacing="4",
        width="100%",
        align="stretch",
    )
