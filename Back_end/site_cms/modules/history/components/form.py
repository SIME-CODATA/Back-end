import reflex as rx

from Back_end.site_cms.components.editor.common import (
    CARD_BG,
    CARD_BORDER,
    SOFT_BG,
    TEXT_MUTED,
    TEXT_PRIMARY,
    text_field,
)
from Back_end.site_cms.state.section_editor_state import (
    SectionEditorState,
)


STANDARD_BLUE = "#1281AA"
STANDARD_PURPLE = "#292561"


def _color_select(
    *,
    index,
    field: str,
) -> rx.Component:
    return rx.select.root(
        rx.select.trigger(
            placeholder="Cores padrão",
            width="145px",
        ),
        rx.select.content(
            rx.select.item(
                "Azul Claro PdM · #1281AA",
                value=STANDARD_BLUE,
            ),
            rx.select.item(
                "Azul Escuro PdM · #292561",
                value=STANDARD_PURPLE,
            ),
            position="popper",
        ),
        on_change=lambda value: (
            SectionEditorState.update_history_card_field(
                index,
                field,
                value,
            )
        ),
    )


def _color_field(
    *,
    label: str,
    value,
    index,
    field: str,
) -> rx.Component:
    return rx.vstack(
        rx.text(
            label,
            color=TEXT_PRIMARY,
            font_size="0.8rem",
            font_weight="600",
        ),
        rx.hstack(
            rx.box(
                width="34px",
                min_width="34px",
                height="34px",
                border_radius="8px",
                background=value,
                border=f"1px solid {CARD_BORDER}",
            ),
            rx.input(
                value=value,
                on_change=lambda new_value: (
                    SectionEditorState.update_history_card_field(
                        index,
                        field,
                        new_value,
                    )
                ),
                placeholder="#1281AA",
                width="150px",
            ),
            _color_select(
                index=index,
                field=field,
            ),
            spacing="2",
            align="center",
            wrap="wrap",
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def _document_type_select(
    document,
    document_index,
) -> rx.Component:
    return rx.vstack(
        rx.text(
            "Tipo",
            color=TEXT_PRIMARY,
            font_size="0.78rem",
            font_weight="600",
        ),
        rx.select.root(
            rx.select.trigger(
                placeholder="Tipo",
                width="100%",
            ),
            rx.select.content(
                rx.select.item(
                    "PDM / documento do programa",
                    value="pdm",
                ),
                rx.select.item(
                    "Relatório",
                    value="relatorio",
                ),
                position="popper",
            ),
            value=document["type"],
            on_change=lambda value: (
                SectionEditorState.update_history_document_field(
                    document_index,
                    "type",
                    value,
                )
            ),
        ),
        spacing="2",
        align="stretch",
        width="100%",
    )


def _document_row(
    document,
    document_index,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        tag="file_text",
                        size=15,
                        color="#1281AA",
                    ),
                    rx.text(
                        "Documento",
                        color=TEXT_PRIMARY,
                        font_size="0.8rem",
                        font_weight="700",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(
                        tag="trash_2",
                        size=13,
                    ),
                    "Remover",
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=lambda: (
                        SectionEditorState.remove_history_document(
                            document_index
                        )
                    ),
                ),
                width="100%",
                align="center",
            ),

            _document_type_select(
                document,
                document_index,
            ),

            text_field(
                label="Nome do documento",
                value=document["name"],
                on_change=lambda value: (
                    SectionEditorState.update_history_document_field(
                        document_index,
                        "name",
                        value,
                    )
                ),
                placeholder=(
                    "Ex.: Versão Final-Participativa "
                    "ou Relatório Anual (2025)"
                ),
            ),

            text_field(
                label="Link do documento",
                value=document["url"],
                on_change=lambda value: (
                    SectionEditorState.update_history_document_field(
                        document_index,
                        "url",
                        value,
                    )
                ),
                placeholder="https://...",
            ),

            spacing="3",
            align="stretch",
            width="100%",
        ),
        width="100%",
        padding="0.9rem",
        background=SOFT_BG,
        border_radius="9px",
    )


def _document_for_card(
    document,
    document_index,
    card_key,
) -> rx.Component:
    return rx.cond(
        document["card_key"] == card_key,
        _document_row(
            document,
            document_index,
        ),
        rx.box(),
    )


def _image_placeholder(
    item,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.icon(
                tag="image",
                size=25,
                color="#1281AA",
            ),
            rx.text(
                "Prévia da imagem do card",
                color=TEXT_PRIMARY,
                font_size="0.78rem",
                font_weight="600",
            ),
            rx.text(
                rx.cond(
                    item["image_url"] != "",
                    "Referência atual preservada no CMS",
                    "Nenhuma imagem vinculada",
                ),
                color=TEXT_MUTED,
                font_size="0.68rem",
            ),
            rx.button(
                "Selecionar imagem",
                size="1",
                variant="soft",
                disabled=True,
                title=(
                    "Será conectado ao Banco de Imagens "
                    "na etapa de mídia."
                ),
            ),
            spacing="2",
            align="center",
        ),
        width="100%",
        min_height="135px",
        display="flex",
        align_items="center",
        justify_content="center",
        padding="1rem",
        background=SOFT_BG,
        border=f"1px dashed {CARD_BORDER}",
        border_radius="10px",
    )


def _history_card(
    item,
    index,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            # Cabeçalho compacto.
            rx.grid(
                text_field(
                    label="Identificador do card",
                    value=item["card_id"],
                    on_change=lambda value: (
                        SectionEditorState.update_history_card_field(
                            index,
                            "card_id",
                            value,
                        )
                    ),
                    placeholder="pdm-2008-2011",
                ),
                text_field(
                    label="Ordem do card",
                    value=item["order"],
                    on_change=lambda value: (
                        SectionEditorState.update_history_card_field(
                            index,
                            "order",
                            value,
                        )
                    ),
                    help_text=(
                        "Define a posição deste card no frontend."
                    ),
                ),
                columns={
                    "initial": "1",
                    "md": "2",
                },
                spacing="4",
                width="100%",
            ),

            # Cores: hexadecimal direto OU dropdown com os padrões.
            rx.grid(
                _color_field(
                    label="Cor principal do card",
                    value=item["primary_color"],
                    index=index,
                    field="primary_color",
                ),
                _color_field(
                    label="Cor do botão",
                    value=item["button_color"],
                    index=index,
                    field="button_color",
                ),
                columns={
                    "initial": "1",
                    "lg": "2",
                },
                spacing="4",
                width="100%",
            ),

            _image_placeholder(
                item
            ),

            rx.box(
                rx.hstack(
                    rx.icon(
                        tag="info",
                        size=14,
                        color="#1281AA",
                    ),
                    rx.text(
                        (
                            "PDM = versões/documentos do Programa de Metas. "
                            "Relatório = balanços e relatórios anuais/finais."
                        ),
                        color=TEXT_MUTED,
                        font_size="0.7rem",
                        line_height="1.4",
                    ),
                    spacing="2",
                    align="start",
                ),
                width="100%",
                padding="0.7rem 0.8rem",
                background=SOFT_BG,
                border_radius="8px",
            ),

            # Documentos do card.
            rx.vstack(
                rx.foreach(
                    SectionEditorState.history_documents,
                    lambda document, document_index: (
                        _document_for_card(
                            document,
                            document_index,
                            item["editor_key"],
                        )
                    ),
                ),
                spacing="3",
                width="100%",
                align="stretch",
            ),

            rx.hstack(
                rx.button(
                    rx.icon(
                        tag="plus",
                        size=14,
                    ),
                    "Adicionar documento",
                    size="2",
                    variant="soft",
                    on_click=lambda: (
                        SectionEditorState.add_history_document(
                            item["editor_key"]
                        )
                    ),
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(
                        tag="trash_2",
                        size=14,
                    ),
                    "Remover card",
                    size="2",
                    variant="soft",
                    color_scheme="red",
                    on_click=lambda: (
                        SectionEditorState.remove_history_card(
                            index
                        )
                    ),
                ),
                width="100%",
                align="center",
                wrap="wrap",
            ),

            spacing="4",
            align="stretch",
            width="100%",
        ),
        width="100%",
        padding="1.15rem",
        background=CARD_BG,
        border=f"1px solid {CARD_BORDER}",
        border_radius="14px",
    )


def history_form() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "Cards do Histórico",
                    size="5",
                    color=TEXT_PRIMARY,
                ),
                rx.text(
                    (
                        "Cada card contém apenas o identificador, ordem, "
                        "cores, imagem e seus documentos."
                    ),
                    color=TEXT_MUTED,
                    font_size="0.76rem",
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.icon(
                    tag="plus",
                    size=14,
                ),
                "Adicionar card",
                size="2",
                variant="soft",
                on_click=SectionEditorState.add_history_card,
            ),
            width="100%",
            align="center",
            wrap="wrap",
        ),

        rx.vstack(
            rx.foreach(
                SectionEditorState.history_cards,
                _history_card,
            ),
            spacing="5",
            width="100%",
            align="stretch",
        ),

        spacing="4",
        width="100%",
        align="stretch",
    )
