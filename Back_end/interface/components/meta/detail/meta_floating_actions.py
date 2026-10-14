import reflex as rx

from Back_end.interface.state.meta.meta_detail_state import (
    MetaDetailState,
)

from Back_end.interface.theme.semantic import (
    BORDER,
    BORDER_DARK,
    SURFACE,
    SURFACE_DARK,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
)


# ============================================================
# CORES
# ============================================================

FLOAT_BACKGROUND = (
    rx.color_mode_cond(
        SURFACE,
        SURFACE_DARK,
    )
)

FLOAT_BORDER = (
    rx.color_mode_cond(
        BORDER,
        BORDER_DARK,
    )
)

BUTTON_BACKGROUND = (
    rx.color_mode_cond(
        "#FFFFFF",
        "#20335F",
    )
)

BUTTON_BACKGROUND_HOVER = (
    rx.color_mode_cond(
        "#EEF3F7",
        "#2C4784",
    )
)

BUTTON_TEXT = (
    rx.color_mode_cond(
        "#272361",
        "#FFFFFF",
    )
)


# ============================================================
# BOTÃO
# ============================================================

def floating_action_button(
    icon: str,
    label: str,
    on_click=None,
    disabled=False,
) -> rx.Component:
    """Botão individual da barra flutuante."""

    return rx.button(
        rx.icon(
            tag=icon,
            size=16,
        ),

        rx.text(
            label,
            font_family=(
                FONT_FAMILY_PRIMARY
            ),
            font_size="0.76rem",
            font_weight="600",
        ),

        on_click=on_click,

        disabled=disabled,

        height="38px",

        padding_x="0.75rem",

        background=(
            BUTTON_BACKGROUND
        ),

        color=BUTTON_TEXT,

        border="none",

        border_radius="9px",

        cursor=rx.cond(
            disabled,
            "not-allowed",
            "pointer",
        ),

        opacity=rx.cond(
            disabled,
            "0.45",
            "1",
        ),

        _hover={
            "background": (
                BUTTON_BACKGROUND_HOVER
            ),
        },

        aria_label=label,
    )


# ============================================================
# BARRA FLUTUANTE
# ============================================================

def meta_floating_actions() -> rx.Component:
    """
    Barra horizontal fixa da Ficha da Meta.

    Ordem:
    próxima | imprimir | buscar | anterior
    """

    return rx.box(
        rx.hstack(

            # =================================================
            # PRÓXIMA
            # =================================================

            floating_action_button(
                icon="chevron-down",
                label="Próxima",

                on_click=(
                    MetaDetailState
                    .go_to_next_meta
                ),

                disabled=(
                    MetaDetailState
                    .codigo_proximo
                    == ""
                ),
            ),

            # =================================================
            # IMPRIMIR
            # =================================================

            floating_action_button(
                icon="printer",
                label="Imprimir",
                
                on_click=(
                    MetaDetailState
                    .open_print_selector
                ),
            ),

            # =================================================
            # BUSCAR
            # =================================================

            floating_action_button(
                icon="search",
                label="Buscar",

                on_click=(
                    MetaDetailState
                    .open_search
                ),
            ),

            # =================================================
            # ANTERIOR
            # =================================================

            floating_action_button(
                icon="chevron-up",
                label="Anterior",

                on_click=(
                    MetaDetailState
                    .go_to_previous_meta
                ),

                disabled=(
                    MetaDetailState
                    .codigo_anterior
                    == ""
                ),
            ),

            spacing="1",
            align="center",
        ),

        # ====================================================
        # POSIÇÃO
        # ====================================================

        position="fixed",

        top="calc(100dvh - 5rem)",

        right="2rem",

        bottom="auto",

        left="auto",

        # ====================================================
        # VISUAL
        # ====================================================

        padding="0.4rem",

        background=(
            FLOAT_BACKGROUND
        ),

        border=(
            f"1px solid "
            f"{FLOAT_BORDER}"
        ),

        border_radius="12px",

        box_shadow=(
            rx.color_mode_cond(
                (
                    "0 6px 20px "
                    "rgba(30, 44, 70, 0.14)"
                ),
                (
                    "0 6px 24px "
                    "rgba(0, 0, 0, 0.30)"
                ),
            )
        ),

        max_width=(
            "calc(100vw - 4rem)"
        ),

        overflow_x="auto",

        z_index="1000",
    )