import reflex as rx

from Back_end.site_cms.components.editor.common import (
    CARD_BG,
    CARD_BORDER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    section_box,
    text_field,
)
from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


def _news_card(item, index) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Notícia ",
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
                        SectionEditorState.remove_news_item(
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
                    SectionEditorState.update_news_title(
                        index,
                        value,
                    )
                ),
            ),

            text_field(
                label="Link",
                value=item["url"],
                on_change=lambda value: (
                    SectionEditorState.update_news_url(
                        index,
                        value,
                    )
                ),
            ),

            rx.grid(
                text_field(
                    label="Data",
                    value=item["date"],
                    on_change=lambda value: (
                        SectionEditorState.update_news_date(
                            index,
                            value,
                        )
                    ),
                    help_text="Formato atual: DD/MM/AAAA",
                ),
                text_field(
                    label="Prioridade",
                    value=item["priority"],
                    on_change=lambda value: (
                        SectionEditorState.update_news_priority(
                            index,
                            value,
                        )
                    ),
                    help_text="Maior valor = maior destaque.",
                ),
                columns={
                    "initial": "1",
                    "md": "2",
                },
                spacing="3",
                width="100%",
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


def news_form() -> rx.Component:
    return section_box(
        "Notícias da Página Inicial",
        (
            "Cadastre, edite e remova as notícias exibidas "
            "na seção do site."
        ),
        rx.hstack(
            rx.text(
                SectionEditorState.news_count,
                " notícia(s)",
                color=TEXT_MUTED,
                font_size="0.75rem",
            ),
            rx.spacer(),
            rx.button(
                rx.icon(
                    tag="plus",
                    size=14,
                ),
                "Adicionar notícia",
                size="2",
                on_click=SectionEditorState.add_news_item,
                variant="soft",
            ),
            width="100%",
            align="center",
        ),
        rx.vstack(
            rx.foreach(
                SectionEditorState.news_items,
                _news_card,
            ),
            spacing="3",
            width="100%",
            align="stretch",
        ),
    )
