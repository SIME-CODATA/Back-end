import reflex as rx

from Back_end.site_cms.components.editor.common import (
    CARD_BG,
    CARD_BORDER,
    TEXT_PRIMARY,
    section_box,
    text_field,
    textarea_field,
)
from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


def _resource_card(item, index) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Recurso ",
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
                        SectionEditorState.remove_transparency_card(
                            index
                        )
                    ),
                ),
                width="100%",
                align="center",
            ),

            text_field(
                label="Título",
                value=item["title"],
                on_change=lambda value: (
                    SectionEditorState.update_transparency_card_title(
                        index,
                        value,
                    )
                ),
            ),

            textarea_field(
                label="Texto",
                value=item["text"],
                on_change=lambda value: (
                    SectionEditorState.update_transparency_card_text(
                        index,
                        value,
                    )
                ),
                min_height="170px",
            ),

            rx.grid(
                text_field(
                    label="Ordem",
                    value=item["order"],
                    on_change=lambda value: (
                        SectionEditorState.update_transparency_card_order(
                            index,
                            value,
                        )
                    ),
                ),
                text_field(
                    label="Texto do botão",
                    value=item["button_label"],
                    on_change=lambda value: (
                        SectionEditorState.update_transparency_button_label(
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

            text_field(
                label="Link do botão",
                value=item["button_url"],
                on_change=lambda value: (
                    SectionEditorState.update_transparency_button_url(
                        index,
                        value,
                    )
                ),
            ),

            spacing="3",
            align="stretch",
            width="100%",
        ),
        width="100%",
        padding="1rem",
        background=CARD_BG,
        border=f"1px solid {CARD_BORDER}",
        border_radius="10px",
    )


def transparency_form() -> rx.Component:
    return rx.vstack(
        section_box(
            "Cabeçalho",
            "Textos que apresentam a seção.",
            text_field(
                label="Título",
                value=SectionEditorState.transparency_title,
                on_change=SectionEditorState.set_transparency_title,
            ),
            text_field(
                label="Subtítulo",
                value=SectionEditorState.transparency_subtitle,
                on_change=SectionEditorState.set_transparency_subtitle,
            ),
        ),

        section_box(
            "Recursos de transparência",
            (
                "Cada item vira um card com texto e botão "
                "na Página Inicial."
            ),
            rx.hstack(
                rx.spacer(),
                rx.button(
                    rx.icon(
                        tag="plus",
                        size=14,
                    ),
                    "Adicionar recurso",
                    size="2",
                    on_click=SectionEditorState.add_transparency_card,
                    variant="soft",
                ),
                width="100%",
            ),
            rx.vstack(
                rx.foreach(
                    SectionEditorState.transparency_cards,
                    _resource_card,
                ),
                spacing="3",
                width="100%",
                align="stretch",
            ),
        ),

        spacing="4",
        width="100%",
        align="stretch",
    )
