import reflex as rx

from Back_end.site_cms.components.editor.common import (
    CARD_BG,
    CARD_BORDER,
    SOFT_BG,
    TEXT_MUTED,
    TEXT_PRIMARY,
)
from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


def _paragraph_preview(
    text,
) -> rx.Component:
    return rx.box(
        rx.text(
            text,
            color=TEXT_PRIMARY,
            font_size="0.8rem",
            line_height="1.5",
        ),
        padding="0.7rem 0.8rem",
        background=SOFT_BG,
        border_radius="8px",
        width="100%",
    )


def _about_preview() -> rx.Component:
    return rx.vstack(
        rx.heading(
            SectionEditorState.letter_title,
            size="5",
            color=TEXT_PRIMARY,
        ),
        rx.text(
            SectionEditorState.letter_author,
            color=TEXT_MUTED,
            font_size="0.82rem",
        ),
        rx.text(
            SectionEditorState.letter_paragraphs_text,
            color=TEXT_PRIMARY,
            white_space="pre-wrap",
            line_height="1.55",
            font_size="0.82rem",
        ),
        spacing="3",
        align="stretch",
        width="100%",
    )


def _news_preview_card(item) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                item["title"],
                color=TEXT_PRIMARY,
                font_size="0.82rem",
                font_weight="600",
            ),
            rx.text(
                item["date"],
                color=TEXT_MUTED,
                font_size="0.7rem",
            ),
            rx.text(
                item["url"],
                color="#1281AA",
                font_size="0.68rem",
            ),
            spacing="1",
            align="start",
        ),
        width="100%",
        padding="0.7rem",
        background=SOFT_BG,
        border_radius="8px",
    )


def _news_preview() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Notícias",
            size="5",
            color=TEXT_PRIMARY,
        ),
        rx.foreach(
            SectionEditorState.news_items,
            _news_preview_card,
        ),
        spacing="2",
        width="100%",
        align="stretch",
    )


def _axis_preview_card(item) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="10px",
                    height="10px",
                    border_radius="50%",
                    background=item["primary_color"],
                ),
                rx.text(
                    item["name"],
                    color=TEXT_PRIMARY,
                    font_weight="700",
                    font_size="0.82rem",
                ),
                spacing="2",
                align="center",
            ),
            rx.text(
                item["title"],
                color=TEXT_MUTED,
                font_size="0.72rem",
            ),
            spacing="1",
            align="start",
        ),
        width="100%",
        padding="0.7rem",
        background=SOFT_BG,
        border_radius="8px",
    )


def _axes_preview() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Eixos",
            size="5",
            color=TEXT_PRIMARY,
        ),
        rx.foreach(
            SectionEditorState.axes_items,
            _axis_preview_card,
        ),
        spacing="2",
        width="100%",
        align="stretch",
    )


def _transparency_preview_card(item) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                item["title"],
                color=TEXT_PRIMARY,
                font_weight="600",
                font_size="0.82rem",
            ),
            rx.text(
                item["text"],
                color=TEXT_MUTED,
                font_size="0.72rem",
                line_height="1.45",
            ),
            rx.text(
                item["button_label"],
                color="#1281AA",
                font_size="0.7rem",
                font_weight="600",
            ),
            spacing="2",
            align="start",
        ),
        width="100%",
        padding="0.7rem",
        background=SOFT_BG,
        border_radius="8px",
    )


def _transparency_preview() -> rx.Component:
    return rx.vstack(
        rx.heading(
            SectionEditorState.transparency_title,
            size="5",
            color=TEXT_PRIMARY,
        ),
        rx.text(
            SectionEditorState.transparency_subtitle,
            color=TEXT_MUTED,
            font_size="0.78rem",
        ),
        rx.foreach(
            SectionEditorState.transparency_cards,
            _transparency_preview_card,
        ),
        spacing="2",
        width="100%",
        align="stretch",
    )


def _history_preview_card(item) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        item["card_id"],
                        color=TEXT_PRIMARY,
                        font_weight="700",
                        font_size="0.84rem",
                    ),
                    rx.text(
                        "Ordem: ",
                        item["order"],
                        color=TEXT_MUTED,
                        font_size="0.7rem",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.box(
                        width="12px",
                        height="12px",
                        border_radius="50%",
                        background=item["primary_color"],
                    ),
                    rx.box(
                        width="12px",
                        height="12px",
                        border_radius="50%",
                        background=item["button_color"],
                    ),
                    spacing="2",
                    align="center",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                "Imagem e documentos vinculados ao card serão "
                "exibidos pelo frontend conforme a publicação.",
                color=TEXT_MUTED,
                font_size="0.7rem",
                line_height="1.4",
            ),
            spacing="2",
            align="start",
        ),
        width="100%",
        padding="0.75rem",
        background=SOFT_BG,
        border_radius="8px",
    )


def _history_preview() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "Histórico",
            size="5",
            color=TEXT_PRIMARY,
        ),
        rx.foreach(
            SectionEditorState.history_cards,
            _history_preview_card,
        ),
        spacing="2",
        width="100%",
        align="stretch",
    )


def _regionalization_preview() -> rx.Component:
    return rx.vstack(
        rx.heading(
            SectionEditorState.regionalization_title,
            size="5",
            color=TEXT_PRIMARY,
        ),
        rx.text(
            SectionEditorState.regionalization_subtitle,
            color=TEXT_MUTED,
            font_size="0.8rem",
        ),
        rx.text(
            SectionEditorState.regionalization_instruction,
            color="#1281AA",
            font_size="0.76rem",
            font_weight="600",
        ),
        rx.text(
            SectionEditorState.regionalization_body,
            color=TEXT_PRIMARY,
            font_size="0.78rem",
            line_height="1.5",
        ),
        rx.text(
            SectionEditorState.regionalization_dashboard_url,
            color="#1281AA",
            font_size="0.7rem",
        ),
        spacing="3",
        width="100%",
        align="stretch",
    )



def _site_about_preview() -> rx.Component:
    return rx.vstack(
        rx.text(
            SectionEditorState.site_about_eyebrow,
            color="#1281AA",
            font_size="0.72rem",
            font_weight="700",
        ),
        rx.heading(
            SectionEditorState.site_about_title,
            size="5",
            color=TEXT_PRIMARY,
        ),
        rx.text(
            SectionEditorState.site_about_subtitle,
            color=TEXT_MUTED,
            font_size="0.8rem",
        ),
        _paragraph_preview(
            SectionEditorState.site_about_what
        ),
        _paragraph_preview(
            SectionEditorState.site_about_why
        ),
        _paragraph_preview(
            SectionEditorState.site_about_for_whom
        ),
        rx.text(
            "Objetivos, metodologia, indicadores e participação "
            "permanecem editáveis neste módulo.",
            color=TEXT_MUTED,
            font_size="0.72rem",
        ),
        spacing="3",
        width="100%",
        align="stretch",
    )


def preview_content(
    section_key: str,
) -> rx.Component:
    if section_key == "about_pdm":
        return _about_preview()

    if section_key == "about":
        return _site_about_preview()

    if section_key == "news":
        return _news_preview()

    if section_key == "axes":
        return _axes_preview()

    if section_key == "transparency":
        return _transparency_preview()

    if section_key == "history":
        return _history_preview()

    if section_key == "regionalization":
        return _regionalization_preview()

    return rx.text(
        "Preview indisponível.",
        color=TEXT_MUTED,
    )


def preview_dialog(
    section_key: str,
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "PREVIEW",
                            color="#1281AA",
                            font_size="0.72rem",
                            font_weight="700",
                            letter_spacing="0.08em",
                        ),
                        rx.heading(
                            SectionEditorState.section_name,
                            size="5",
                            color=TEXT_PRIMARY,
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon(
                            tag="x",
                            size=15,
                        ),
                        on_click=SectionEditorState.close_preview,
                        variant="ghost",
                    ),
                    width="100%",
                    align="center",
                ),

                rx.box(
                    preview_content(
                        section_key
                    ),
                    width="100%",
                    padding="1rem",
                    background=CARD_BG,
                    border=f"1px solid {CARD_BORDER}",
                    border_radius="12px",
                ),

                rx.hstack(
                    rx.spacer(),
                    rx.button(
                        "Fechar preview",
                        on_click=SectionEditorState.close_preview,
                        variant="soft",
                    ),
                    width="100%",
                ),

                spacing="4",
                width="100%",
                align="stretch",
            ),
            max_width="900px",
            width="92vw",
            max_height="88vh",
            overflow_y="auto",
        ),
        open=SectionEditorState.preview_open,
    )
