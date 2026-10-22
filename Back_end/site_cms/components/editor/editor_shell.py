import reflex as rx

from Back_end.site_cms.components.editor.common import (
    CARD_BG,
    CARD_BORDER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    action_bar,
    messages,
    publication_note,
    version_history,
)
from Back_end.site_cms.components.editor.preview import (
    preview_dialog,
)
from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


def section_editor_content(
    *,
    section_key: str,
    icon: str,
    form: rx.Component,
) -> rx.Component:
    """Estrutura comum a todos os seis editores da Home."""

    return rx.cond(
        SectionEditorState.loading,
        rx.box(
            rx.vstack(
                rx.spinner(
                    size="3"
                ),
                rx.text(
                    "Carregando módulo do CMS...",
                    color=TEXT_MUTED,
                ),
                spacing="3",
                align="center",
            ),
            width="100%",
            padding="4rem",
        ),
        rx.vstack(
            preview_dialog(
                section_key
            ),

            rx.link(
                rx.hstack(
                    rx.icon(
                        tag="arrow_left",
                        size=14,
                    ),
                    rx.text(
                        "Voltar para Página Inicial",
                        font_size="0.78rem",
                    ),
                    spacing="2",
                    align="center",
                ),
                href="/admin/site/",
                color="#1281AA",
                text_decoration="none",
            ),

            messages(),

            rx.hstack(
                rx.box(
                    rx.icon(
                        tag=icon,
                        size=24,
                        color="#FFFFFF",
                    ),
                    width="52px",
                    min_width="52px",
                    height="52px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    border_radius="14px",
                    background="#1281AA",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            SectionEditorState.section_name,
                            size="7",
                            color=TEXT_PRIMARY,
                        ),
                        rx.box(
                            rx.text(
                                SectionEditorState.status_label,
                                font_size="0.72rem",
                                font_weight="600",
                            ),
                            padding="0.25rem 0.6rem",
                            border_radius="999px",
                            background=rx.cond(
                                SectionEditorState.has_draft,
                                "#FFF3CD",
                                "#DCFCE7",
                            ),
                            color=rx.cond(
                                SectionEditorState.has_draft,
                                "#7A5B00",
                                "#166534",
                            ),
                        ),
                        spacing="3",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.text(
                        SectionEditorState.section_description,
                        color=TEXT_MUTED,
                        font_size="0.9rem",
                    ),
                    rx.hstack(
                        rx.text(
                            SectionEditorState.source_label,
                            color=TEXT_MUTED,
                            font_size="0.72rem",
                        ),
                        rx.text(
                            "•",
                            color=TEXT_MUTED,
                            font_size="0.72rem",
                        ),
                        rx.text(
                            SectionEditorState.enabled_label,
                            color=TEXT_MUTED,
                            font_size="0.72rem",
                        ),
                        rx.text(
                            "•",
                            color=TEXT_MUTED,
                            font_size="0.72rem",
                        ),
                        rx.text(
                            "Atualizado: ",
                            SectionEditorState.updated_label,
                            color=TEXT_MUTED,
                            font_size="0.72rem",
                        ),
                        spacing="2",
                        wrap="wrap",
                    ),
                    spacing="2",
                    align="start",
                    flex="1",
                ),
                width="100%",
                align="start",
                spacing="4",
            ),

            rx.grid(
                rx.vstack(
                    form,
                    publication_note(),
                    action_bar(),
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),

                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(
                                    tag="eye",
                                    size=16,
                                    color="#1281AA",
                                ),
                                rx.heading(
                                    "Como funciona",
                                    size="4",
                                    color=TEXT_PRIMARY,
                                ),
                                spacing="2",
                                align="center",
                            ),
                            rx.text(
                                (
                                    "As alterações ficam no rascunho até "
                                    "uma nova publicação. O site público "
                                    "continua recebendo a versão publicada."
                                ),
                                color=TEXT_MUTED,
                                font_size="0.76rem",
                                line_height="1.45",
                            ),
                            rx.text(
                                "Editar → Rascunho → Preview → Publicar",
                                color="#1281AA",
                                font_size="0.75rem",
                                font_weight="600",
                            ),
                            spacing="3",
                            align="start",
                        ),
                        width="100%",
                        padding="1rem",
                        background=CARD_BG,
                        border=f"1px solid {CARD_BORDER}",
                        border_radius="12px",
                    ),
                    version_history(),
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),

                columns={
                    "initial": "1",
                    "lg": "1fr 360px",
                },
                spacing="5",
                width="100%",
            ),

            width="100%",
            max_width="1280px",
            margin="0 auto",
            spacing="5",
            align="stretch",
        ),
    )
