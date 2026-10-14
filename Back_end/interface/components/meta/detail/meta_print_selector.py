import reflex as rx

from Back_end.interface.state.meta.meta_detail_state import (
    MetaDetailState,
    MetaPrintOption,
)

from Back_end.interface.theme.semantic import (
    BORDER,
    BORDER_DARK,
    SURFACE,
    SURFACE_DARK,
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)


MODAL_BACKGROUND = rx.color_mode_cond(
    SURFACE,
    SURFACE_DARK,
)

MODAL_BORDER = rx.color_mode_cond(
    BORDER,
    BORDER_DARK,
)

MODAL_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

MODAL_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)


def print_option_item(
    option: rx.Var[MetaPrintOption],
) -> rx.Component:
    """Item selecionável de uma meta."""

    return rx.box(
        rx.hstack(
            rx.checkbox(
                checked=option["selected"],

                on_change=lambda checked: (
                    MetaDetailState
                    .set_print_meta_selected(
                        option["codigo"],
                        checked,
                    )
                ),
            ),

            rx.vstack(
                rx.text(
                    "META ",
                    option["codigo"],

                    color="#288140",

                    font_family=(
                        FONT_FAMILY_SECUNDARY
                    ),

                    font_size="0.9rem",
                ),

                rx.text(
                    option["titulo"],

                    color=MODAL_TEXT,

                    font_family=(
                        FONT_FAMILY_PRIMARY
                    ),

                    font_size="0.76rem",

                    line_height="1.25",

                    overflow="hidden",

                    text_overflow="ellipsis",

                    style={
                        "display": "-webkit-box",
                        "-webkit-line-clamp": "2",
                        "-webkit-box-orient": "vertical",
                    },
                ),

                spacing="1",

                align="start",

                min_width="0",

                flex="1",
            ),

            spacing="3",

            align="start",

            width="100%",
        ),

        width="100%",

        padding="0.75rem",

        border=f"1px solid {MODAL_BORDER}",

        border_radius="10px",

        background=rx.cond(
            option["selected"],

            rx.color_mode_cond(
                "#F0F8F2",
                "rgba(40,129,64,0.13)",
            ),

            MODAL_BACKGROUND,
        ),
    )


def meta_print_selector() -> rx.Component:
    """Modal para seleção das fichas a imprimir."""

    return rx.box(

        # ====================================================
        # OVERLAY
        # ====================================================

        rx.box(
            position="fixed",

            inset="0",

            background=(
                "rgba(10, 18, 35, 0.55)"
            ),

            backdrop_filter="blur(2px)",

            z_index="1200",

            on_click=(
                MetaDetailState
                .close_print_selector
            ),
        ),

        # ====================================================
        # MODAL
        # ====================================================

        rx.box(
            rx.vstack(

                # ------------------------------------------------
                # Header
                # ------------------------------------------------

                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "IMPRIMIR FICHAS",

                            color=MODAL_TEXT,

                            font_family=(
                                FONT_FAMILY_SECUNDARY
                            ),

                            font_size="1.4rem",

                            line_height="1",
                        ),

                        rx.text(
                            "Selecione uma ou mais metas "
                            "para gerar um único documento.",

                            color=MODAL_MUTED,

                            font_family=(
                                FONT_FAMILY_PRIMARY
                            ),

                            font_size="0.8rem",
                        ),

                        spacing="2",

                        align="start",
                    ),

                    rx.spacer(),

                    rx.button(
                        rx.icon(
                            tag="x",
                            size=18,
                        ),

                        on_click=(
                            MetaDetailState
                            .close_print_selector
                        ),

                        variant="ghost",

                        color=MODAL_TEXT,

                        cursor="pointer",
                    ),

                    width="100%",

                    align="start",
                ),

                rx.divider(),

                # ------------------------------------------------
                # Pesquisa + comandos
                # ------------------------------------------------

                rx.flex(
                    rx.input(
                        rx.input.slot(
                            rx.icon(
                                tag="search",
                                size=17,
                            ),
                        ),

                        placeholder=(
                            "Pesquisar por número "
                            "ou título..."
                        ),

                        value=(
                            MetaDetailState
                            .print_search_text
                        ),

                        on_change=(
                            MetaDetailState
                            .update_print_search
                        ),

                        width="100%",

                        max_width="380px",
                    ),

                    rx.button(
                        "SELECIONAR TODAS",

                        on_click=(
                            MetaDetailState
                            .select_all_print_metas
                        ),

                        variant="outline",

                        cursor="pointer",
                    ),

                    rx.button(
                        "LIMPAR",

                        on_click=(
                            MetaDetailState
                            .clear_print_selection
                        ),

                        variant="ghost",

                        cursor="pointer",
                    ),

                    gap="0.6rem",

                    align="center",

                    wrap="wrap",

                    width="100%",
                ),

                # ------------------------------------------------
                # Quantidade
                # ------------------------------------------------

                rx.text(
                    MetaDetailState
                    .print_selected_count,

                    " ficha(s) selecionada(s)",

                    color=MODAL_MUTED,

                    font_family=(
                        FONT_FAMILY_PRIMARY
                    ),

                    font_size="0.75rem",
                ),

                # ------------------------------------------------
                # Lista
                # ------------------------------------------------

                rx.box(
                    rx.grid(
                        rx.foreach(
                            MetaDetailState
                            .print_options_filtradas,

                            print_option_item,
                        ),

                        columns={
                            "initial": "1",
                            "lg": "2",
                        },

                        spacing="2",

                        width="100%",
                    ),

                    width="100%",

                    max_height="52vh",

                    overflow_y="auto",

                    padding_right="0.25rem",
                ),

                # ------------------------------------------------
                # Erro
                # ------------------------------------------------

                rx.cond(
                    MetaDetailState
                    .print_error
                    != "",

                    rx.text(
                        MetaDetailState
                        .print_error,

                        color="#C62828",

                        font_family=(
                            FONT_FAMILY_PRIMARY
                        ),

                        font_size="0.78rem",
                    ),
                ),

                rx.divider(),

                # ------------------------------------------------
                # Footer
                # ------------------------------------------------

                rx.hstack(
                    rx.button(
                        "CANCELAR",

                        on_click=(
                            MetaDetailState
                            .close_print_selector
                        ),

                        variant="ghost",

                        cursor="pointer",
                    ),

                    rx.spacer(),

                    rx.button(
                        rx.icon(
                            tag="printer",
                            size=16,
                        ),

                        "GERAR DOCUMENTO",

                        on_click=(
                            MetaDetailState
                            .open_print_document
                        ),

                        background="#272361",

                        color="white",

                        cursor="pointer",
                    ),

                    width="100%",

                    align="center",
                ),

                spacing="4",

                align="stretch",

                width="100%",
            ),

            position="fixed",

            top="50%",

            left="50%",

            transform=(
                "translate(-50%, -50%)"
            ),

            width="min(900px, 94vw)",

            max_height="88vh",

            padding="1.25rem",

            background=MODAL_BACKGROUND,

            border=f"1px solid {MODAL_BORDER}",

            border_radius="16px",

            box_shadow=(
                "0 22px 60px "
                "rgba(0,0,0,0.24)"
            ),

            z_index="1201",
        ),

        display=rx.cond(
            MetaDetailState
            .print_selector_open,

            "block",

            "none",
        ),
    )