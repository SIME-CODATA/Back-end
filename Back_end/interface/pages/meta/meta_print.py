import reflex as rx

from Back_end.interface.state.meta.meta_print_state import (
    MetaPrintState,
)

from Back_end.interface.components.meta.print.meta_print_document import (
    meta_print_document,
)

from Back_end.interface.components.meta.print.meta_print_styles import (
    meta_print_styles,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
)


# ============================================================
# TOOLBAR
# ============================================================

def print_toolbar() -> rx.Component:
    """Ações disponíveis na prévia do documento."""

    return rx.hstack(
        rx.link(
            rx.button(
                rx.icon(
                    tag="arrow-left",
                    size=16,
                ),

                "Voltar para ficha",

                variant="outline",

                color="#272361",

                background="white",

                cursor="pointer",
            ),

            href=MetaPrintState.detail_url,

            text_decoration="none",
        ),

        rx.spacer(),

        rx.button(
            rx.icon(
                tag="printer",
                size=16,
            ),

            "IMPRIMIR / SALVAR PDF",

            on_click=(
                MetaPrintState.trigger_print
            ),

            background="#272361",

            color="white",

            font_family=(
                FONT_FAMILY_PRIMARY
            ),

            cursor="pointer",

            _hover={
                "background": "#39357A",
            },
        ),

        rx.button(
            rx.icon(
                tag="x",
                size=16,
            ),

            "FECHAR",

            on_click=(
                MetaPrintState.close_window
            ),

            variant="outline",

            cursor="pointer",
        ),

        class_name="print-toolbar",

        width="100%",

        padding="0.7rem",

        background="white",

        border="1px solid #D8DEE8",

        border_radius="10px",

        box_shadow=(
            "0 5px 18px "
            "rgba(18, 30, 55, 0.08)"
        ),

        align="center",

        spacing="2",
    )


# ============================================================
# CARREGAMENTO
# ============================================================

def print_loading() -> rx.Component:

    return rx.center(
        rx.vstack(
            rx.spinner(
                size="3",
            ),

            rx.text(
                "Preparando documento...",

                color="#667085",

                font_size="0.85rem",
            ),

            spacing="3",
            align="center",
        ),

        min_height="70vh",

        width="100%",
    )


# ============================================================
# ERRO
# ============================================================

def print_error() -> rx.Component:

    return rx.center(
        rx.vstack(
            rx.icon(
                tag="triangle-alert",

                size=28,

                color="#C62828",
            ),

            rx.text(
                "Não foi possível preparar "
                "a Ficha da Meta.",

                color="#17213C",

                font_weight="700",
            ),

            rx.text(
                MetaPrintState.error_message,

                color="#667085",

                font_size="0.82rem",
            ),

            spacing="3",

            align="center",
        ),

        min_height="70vh",

        width="100%",
    )


# ============================================================
# NÃO ENCONTRADA
# ============================================================

def print_not_found() -> rx.Component:

    return rx.center(
        rx.vstack(
            rx.icon(
                tag="file-question",

                size=28,

                color="#667085",
            ),

            rx.text(
                "Meta não encontrada.",

                color="#17213C",

                font_weight="700",
            ),

            spacing="3",

            align="center",
        ),

        min_height="70vh",

        width="100%",
    )


# ============================================================
# PÁGINA
# ============================================================

def meta_print_page() -> rx.Component:
    """Prévia A4 da Ficha da Meta."""

    return rx.box(
        meta_print_styles(),

        rx.cond(
            MetaPrintState.loading,

            print_loading(),

            rx.cond(
                MetaPrintState.error_message
                != "",

                print_error(),

                rx.cond(
                    MetaPrintState.ficha_encontrada,

                    rx.box(
                        print_toolbar(),

                        meta_print_document(),

                        width="100%",
                    ),

                    print_not_found(),
                ),
            ),
        ),

        class_name="meta-print-shell",

        width="100%",
    )