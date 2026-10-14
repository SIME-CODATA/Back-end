import reflex as rx

from Back_end.interface.state.meta.meta_detail_state import (
    MetaDetailState,
)

from Back_end.interface.theme.semantic import (
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


# ============================================================
# CORES
# ============================================================

SEARCH_BACKGROUND = rx.color_mode_cond(
    SURFACE,
    SURFACE_DARK,
)

SEARCH_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

SEARCH_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)


# ============================================================
# PAINEL
# ============================================================

def meta_search_panel() -> rx.Component:
    """
    Painel lateral para localizar e abrir outra meta.
    """

    return rx.box(

        # ====================================================
        # FUNDO ESCURECIDO
        # ====================================================

        rx.box(
            position="fixed",
            inset="0",

            background="rgba(0, 0, 0, 0.35)",

            z_index="1100",
        ),

        # ====================================================
        # PAINEL
        # ====================================================

        rx.box(
            rx.vstack(

                # ------------------------------------------------
                # Cabeçalho
                # ------------------------------------------------

                rx.hstack(
                    rx.text(
                        "BUSCAR META",
                        color=SEARCH_TEXT,
                        font_family=FONT_FAMILY_SECUNDARY,
                        font_size="1.35rem",
                        line_height="1",
                    ),

                    rx.spacer(),

                    rx.button(
                        rx.icon(
                            tag="x",
                            size=18,
                        ),

                        on_click=(
                            MetaDetailState.close_search
                        ),

                        variant="ghost",

                        color=SEARCH_TEXT,

                        cursor="pointer",

                        aria_label="Fechar busca",
                    ),

                    width="100%",
                    align="center",
                ),

                rx.divider(),

                # ------------------------------------------------
                # Descrição
                # ------------------------------------------------

                rx.text(
                    "Digite o número da meta que deseja abrir.",
                    color=SEARCH_MUTED,
                    font_family=FONT_FAMILY_PRIMARY,
                    font_size="0.84rem",
                    line_height="1.4",
                ),

                # ------------------------------------------------
                # Campo
                # ------------------------------------------------

                rx.vstack(
                    rx.text(
                        "Número da meta",
                        color=SEARCH_TEXT,
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.82rem",
                        font_weight="600",
                    ),

                    rx.input(
                        rx.input.slot(
                            rx.icon(
                                tag="search",
                                size=17,
                                color=SEARCH_MUTED,
                            ),
                        ),

                        placeholder="Ex.: 001 ou 25",

                        value=(
                            MetaDetailState
                            .search_codigo
                        ),

                        on_change=(
                            MetaDetailState
                            .update_search_codigo
                        ),

                        width="100%",

                        font_family=FONT_FAMILY_PRIMARY,
                    ),

                    spacing="2",
                    align="stretch",
                    width="100%",
                ),

                # ------------------------------------------------
                # Erro
                # ------------------------------------------------

                rx.cond(
                    MetaDetailState.search_error != "",

                    rx.hstack(
                        rx.icon(
                            tag="triangle-alert",
                            size=15,
                            color="#C62828",
                        ),

                        rx.text(
                            MetaDetailState.search_error,
                            color="#C62828",
                            font_family=FONT_FAMILY_PRIMARY,
                            font_size="0.8rem",
                        ),

                        spacing="2",
                        align="center",
                    ),
                ),

                # ------------------------------------------------
                # Abrir ficha
                # ------------------------------------------------

                rx.button(
                    rx.icon(
                        tag="search",
                        size=16,
                    ),

                    "ABRIR FICHA",

                    on_click=(
                        MetaDetailState.go_to_meta
                    ),

                    width="100%",
                    height="42px",

                    background="#272361",
                    color="white",

                    font_family=FONT_FAMILY_SECUNDARY,
                    font_size="0.92rem",

                    border_radius="10px",

                    cursor="pointer",

                    _hover={
                        "background": "#39357A",
                    },
                ),

                spacing="4",
                align="stretch",
                width="100%",
            ),

            # ====================================================
            # POSIÇÃO
            # ====================================================

            position="fixed",

            top="0",
            left="0",

            width="min(360px, 92vw)",
            height="100dvh",

            background=SEARCH_BACKGROUND,

            padding="1.5rem",

            box_shadow=(
                "0 8px 32px "
                "rgba(0, 0, 0, 0.18)"
            ),

            z_index="1101",

            overflow_y="auto",
        ),

        # ========================================================
        # ABERTO / FECHADO
        # ========================================================

        display=rx.cond(
            MetaDetailState.search_open,
            "block",
            "none",
        ),
    )