import reflex as rx

from Back_end.site_cms.components.editor.common import (
    CARD_BG,
    CARD_BORDER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    media_notice,
    section_box,
    text_field,
    textarea_field,
)
from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


def _axis_card(item, index) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="12px",
                    height="12px",
                    border_radius="50%",
                    background=item["primary_color"],
                ),
                rx.text(
                    item["name"],
                    color=TEXT_PRIMARY,
                    font_size="0.9rem",
                    font_weight="700",
                ),
                rx.spacer(),
                rx.text(
                    "ID legado: ",
                    item["legacy_id"],
                    color=TEXT_MUTED,
                    font_size="0.68rem",
                ),
                width="100%",
                align="center",
            ),

            rx.grid(
                text_field(
                    label="Nome",
                    value=item["name"],
                    on_change=lambda value: (
                        SectionEditorState.update_axis_name(
                            index,
                            value,
                        )
                    ),
                ),
                text_field(
                    label="Título",
                    value=item["title"],
                    on_change=lambda value: (
                        SectionEditorState.update_axis_title(
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
                label="Cor principal",
                value=item["primary_color"],
                on_change=lambda value: (
                    SectionEditorState.update_axis_color(
                        index,
                        value,
                    )
                ),
                help_text="Ex.: #3DB54A",
            ),

            textarea_field(
                label="Destaques",
                value=item["highlights_text"],
                on_change=lambda value: (
                    SectionEditorState.update_axis_highlights(
                        index,
                        value,
                    )
                ),
                help_text="Um item por linha.",
                min_height="130px",
            ),

            textarea_field(
                label="Textos",
                value=item["paragraphs_text"],
                on_change=lambda value: (
                    SectionEditorState.update_axis_paragraphs(
                        index,
                        value,
                    )
                ),
                help_text=(
                    "Separe os parágrafos deixando uma linha em branco."
                ),
                min_height="220px",
            ),

            media_notice(),

            rx.grid(
                text_field(
                    label="Imagem principal atual",
                    value=item["image_url"],
                    on_change=lambda value: (
                        SectionEditorState.update_axis_image_url(
                            index,
                            value,
                        )
                    ),
                ),
                text_field(
                    label="Imagem do card atual",
                    value=item["card_image_url"],
                    on_change=lambda value: (
                        SectionEditorState.update_axis_card_image_url(
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

            spacing="4",
            align="stretch",
            width="100%",
        ),
        width="100%",
        padding="1rem",
        background=CARD_BG,
        border=f"1px solid {CARD_BORDER}",
        border_radius="10px",
    )


def axes_form() -> rx.Component:
    return section_box(
        "Eixos",
        (
            "Cada eixo é editado individualmente. "
            "A ordem atual é preservada pela lista."
        ),
        rx.vstack(
            rx.foreach(
                SectionEditorState.axes_items,
                _axis_card,
            ),
            spacing="4",
            width="100%",
            align="stretch",
        ),
    )
