import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.state.meta.meta_detail_state import MetaDetailState
from Back_end.interface.theme.semantic import (
    BORDER,
    SURFACE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


def info_item(label: str, value) -> rx.Component:
    """Exibe uma informação da meta."""

    return rx.vstack(
        rx.text(
            label,
            color=TEXT_SECONDARY,
            font_size="0.8rem",
            font_weight="600",
        ),
        rx.text(
            value,
            color=TEXT_PRIMARY,
            font_weight="600",
        ),
        spacing="1",
        align="start",
    )


def text_item(value: str) -> rx.Component:
    """Exibe um item de uma lista."""

    return rx.text(
        value,
        color=TEXT_PRIMARY,
        font_size="0.9rem",
    )


def ficha_content() -> rx.Component:
    """Primeira versão da ficha com dados reais."""

    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text(
                    "META ",
                    MetaDetailState.codigo_atual,
                    color="#288140",
                    font_size="0.9rem",
                    font_weight="700",
                ),

                rx.heading(
                    MetaDetailState.titulo,
                    color=TEXT_PRIMARY,
                    size="6",
                ),

                rx.text(
                    MetaDetailState.eixo,
                    color=TEXT_SECONDARY,
                ),

                spacing="3",
                align="start",
            ),

            width="100%",
            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="12px",
            padding="1.5rem",
            position="relative",
        ),
        rx.button(
            rx.icon(tag="search", size=18),
            on_click=MetaDetailState.open_search,
            variant="outline",
            color="#272361",
            background="white",
            border_radius="10px",
            cursor="pointer",
            position="absolute",
            top="1rem",
            right="1rem",
            z_index="1",
            aria_label="Buscar outra meta",
        ),

        rx.box(
            rx.vstack(
                rx.heading(
                    "Informações gerais",
                    size="4",
                    color=TEXT_PRIMARY,
                ),

                rx.grid(
                    info_item(
                        "Andamento",
                        MetaDetailState.andamento,
                    ),

                    info_item(
                        "Situação",
                        MetaDetailState.situacao,
                    ),

                    info_item(
                        "Previsão",
                        MetaDetailState.prazo,
                    ),

                    columns={
                        "initial": "1",
                        "md": "3",
                    },

                    spacing="4",
                    width="100%",
                ),

                rx.divider(),

                rx.text(
                    "Órgãos vinculados",
                    color=TEXT_SECONDARY,
                    font_weight="600",
                ),

                rx.foreach(
                    MetaDetailState.orgaos,
                    text_item,
                ),

                rx.divider(),

                rx.text(
                    "ODS",
                    color=TEXT_SECONDARY,
                    font_weight="600",
                ),

                rx.foreach(
                    MetaDetailState.ods,
                    text_item,
                ),

                spacing="4",
                align="stretch",
            ),

            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="12px",
            padding="1.5rem",
            width="100%",
        ),

        rx.box(
            rx.vstack(
                rx.heading(
                    "Contexto da meta",
                    size="4",
                    color=TEXT_PRIMARY,
                ),

                rx.text(
                    MetaDetailState.contexto,
                    color=TEXT_PRIMARY,
                    white_space="pre-wrap",
                ),

                spacing="3",
                align="stretch",
            ),

            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="12px",
            padding="1.5rem",
            width="100%",
        ),

        rx.box(
            rx.vstack(
                rx.heading(
                    "Orçamento",
                    size="4",
                    color=TEXT_PRIMARY,
                ),

                rx.grid(
                    info_item(
                        "Recursos previstos",
                        MetaDetailState.previsao,
                    ),

                    info_item(
                        "Empenhado",
                        MetaDetailState.empenhado,
                    ),

                    info_item(
                        "Liquidado",
                        MetaDetailState.liquidado,
                    ),

                    columns={
                        "initial": "1",
                        "md": "3",
                    },

                    spacing="4",
                    width="100%",
                ),

                spacing="4",
                align="stretch",
            ),

            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="12px",
            padding="1.5rem",
            width="100%",
        ),

        rx.box(
            rx.vstack(
                rx.heading(
                    "Iniciativas cadastradas",
                    size="4",
                    color=TEXT_PRIMARY,
                ),

                rx.cond(
                    MetaDetailState.iniciativas.length() > 0,

                    rx.vstack(
                        rx.foreach(
                            MetaDetailState.iniciativas,
                            text_item,
                        ),

                        align="stretch",
                        spacing="3",
                    ),

                    rx.text(
                        "Nenhuma iniciativa cadastrada "
                        "para esta meta na fonte consultada.",
                        color=TEXT_SECONDARY,
                    ),
                ),

                spacing="4",
                align="stretch",
            ),

            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="12px",
            padding="1.5rem",
            width="100%",
        ),

        width="100%",
        align="stretch",
        spacing="5",
    )
    
def search_panel() -> rx.Component:
    """Painel lateral que aparece sobre a ficha."""

    return rx.box(
        # Fundo escurecido atrás do painel.
        rx.box(
            position="fixed",
            inset="0",
            background="rgba(0, 0, 0, 0.35)",
            z_index="1100",
        ),

        # Painel de busca.
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "Buscar metas",
                        size="5",
                        color=TEXT_PRIMARY,
                    ),

                    rx.spacer(),

                    rx.button(
                        rx.icon(tag="x", size=18),
                        on_click=MetaDetailState.close_search,
                        variant="ghost",
                        color=TEXT_PRIMARY,
                        cursor="pointer",
                        aria_label="Fechar busca",
                    ),

                    width="100%",
                    align="center",
                ),

                rx.divider(),

                rx.text(
                    "Número da meta",
                    font_weight="600",
                    color=TEXT_PRIMARY,
                    font_size="0.9rem",
                ),

                rx.input(
                    placeholder="Ex.: 001 ou 25",
                    value=MetaDetailState.search_codigo,
                    on_change=MetaDetailState.update_search_codigo,
                    width="100%",
                ),

                rx.cond(
                    MetaDetailState.search_error != "",
                    rx.text(
                        MetaDetailState.search_error,
                        color="#C62828",
                        font_size="0.85rem",
                    ),
                ),

                rx.button(
                    rx.icon(tag="search", size=16),
                    "Abrir ficha",
                    on_click=MetaDetailState.go_to_meta,
                    width="100%",
                    background="#272361",
                    color="white",
                    cursor="pointer",
                ),

                rx.text(
                    "Em seguida, adicionaremos a busca por título "
                    "e os filtros por eixo, órgão e situação.",
                    color=TEXT_SECONDARY,
                    font_size="0.8rem",
                ),

                spacing="4",
                align="stretch",
            ),

            position="fixed",
            top="0",
            left="0",
            width="min(360px, 92vw)",
            height="100dvh",
            background=SURFACE,
            padding="1.5rem",
            box_shadow="0 8px 32px rgba(0, 0, 0, 0.18)",
            z_index="1101",
            overflow_y="auto",
        ),

        # Quando fechado, não ocupa espaço nem cobre a ficha.
        display=rx.cond(
            MetaDetailState.search_open,
            "block",
            "none",
        ),
    )


def meta_detail_content() -> rx.Component:
    """Controla carregamento, erros e exibição da ficha."""

    return rx.vstack(
        search_panel(),
        rx.cond(
            MetaDetailState.loading,

            rx.text(
                "Carregando ficha da meta...",
                color=TEXT_SECONDARY,
            ),

            rx.cond(
                MetaDetailState.error_message != "",

                rx.text(
                    MetaDetailState.error_message,
                    color="#EC2024",
                ),

                rx.cond(
                    MetaDetailState.ficha_encontrada,

                    ficha_content(),

                    rx.text(
                        "Meta não encontrada: ",
                        MetaDetailState.codigo_atual,
                        color=TEXT_SECONDARY,
                    ),
                ),
            ),
        ),

        width="100%",
        align="stretch",
    )


def meta_detail_page() -> rx.Component:
    """Página dinâmica da Ficha da Meta."""

    return admin_layout(
        meta_detail_content()
    )
    