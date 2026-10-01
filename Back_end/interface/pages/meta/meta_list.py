import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.state.meta.meta_list_state import MetaListState

from Back_end.interface.theme.semantic import (
    BORDER,
    SURFACE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


def meta_list_item(meta: rx.Var[dict[str, str]]) -> rx.Component:
    """Card clicável de uma meta."""

    return rx.link(
        rx.hstack(
            rx.vstack(
                rx.text(
                    "META ",
                    meta["codigo"],
                    color="#288140",
                    font_size="0.8rem",
                    font_weight="700",
                ),

                rx.text(
                    meta["titulo"],
                    color=TEXT_PRIMARY,
                    font_size="1rem",
                    font_weight="600",
                ),

                rx.text(
                    meta["eixo"],
                    color=TEXT_SECONDARY,
                    font_size="0.85rem",
                ),

                align="start",
                spacing="2",
                flex="1",
                min_width="0",
            ),

            rx.icon(
                tag="chevron-right",
                size=20,
                color="#272361",
            ),

            align="center",
            width="100%",
            spacing="4",
        ),

        href=meta["url"],
        width="100%",
        padding="1rem",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        text_decoration="none",
        cursor="pointer",

        _hover={
            "border_color": "#272361",
            "background": "#F7F7FC",
        },
    )


def meta_list_content() -> rx.Component:
    """Página de pesquisa e seleção das metas."""

    return rx.vstack(
        rx.vstack(
            rx.heading(
                "Metas",
                size="7",
                color=TEXT_PRIMARY,
            ),

            rx.text(
                "Pesquise e selecione uma meta para visualizar sua ficha.",
                color=TEXT_SECONDARY,
            ),

            spacing="2",
            align="start",
            width="100%",
        ),

        rx.input(
            rx.input.slot(
                rx.icon(tag="search", size=18),
            ),

            placeholder="Pesquisar pelo número ou título da meta...",
            value=MetaListState.search_text,
            on_change=MetaListState.update_search_text,

            width="100%",
            background=SURFACE,
            size="3",
        ),

        rx.cond(
            MetaListState.loading,

            rx.text(
                "Carregando metas...",
                color=TEXT_SECONDARY,
            ),

            rx.cond(
                MetaListState.error_message != "",

                rx.text(
                    MetaListState.error_message,
                    color="#C62828",
                ),

                rx.vstack(
                    rx.text(
                        MetaListState.metas_filtradas.length(),
                        " meta(s) encontrada(s)",
                        color=TEXT_SECONDARY,
                        font_size="0.85rem",
                    ),

                    rx.cond(
                        MetaListState.metas_filtradas.length() > 0,

                        rx.vstack(
                            rx.foreach(
                                MetaListState.metas_filtradas,
                                meta_list_item,
                            ),

                            spacing="3",
                            align="stretch",
                            width="100%",
                        ),

                        rx.text(
                            "Nenhuma meta encontrada para esta pesquisa.",
                            color=TEXT_SECONDARY,
                        ),
                    ),

                    spacing="4",
                    align="stretch",
                    width="100%",
                ),
            ),
        ),

        spacing="5",
        align="stretch",
        width="100%",
    )


def meta_list_page() -> rx.Component:
    """Página administrativa com a lista de metas."""

    return admin_layout(
        meta_list_content()
    )