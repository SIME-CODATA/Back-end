import reflex as rx

from Back_end.interface.theme.semantic import (
    BORDER,
    HEADER_BACKGROUND,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from Back_end.interface.theme.typography import (
    FONT_SIZE_SM,
    FONT_SIZE_LG,
    FONT_WEIGHT_MEDIUM,
    FONT_WEIGHT_SEMIBOLD,
)


def header() -> rx.Component:
    """Cabeçalho principal da interface administrativa."""

    return rx.hstack(
        # Identificação da página
        rx.vstack(
            rx.text(
                "Programa de Metas",
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_LG,
                font_weight=FONT_WEIGHT_SEMIBOLD,
            ),
            rx.text(
                "Painel Administrativo",
                color=TEXT_SECONDARY,
                font_size=FONT_SIZE_SM,
            ),
            spacing="0",
            align="start",
        ),

        rx.spacer(),

        # Área do usuário
        rx.hstack(
            rx.icon(
                tag="bell",
                size=19,
                color=TEXT_SECONDARY,
            ),

            rx.box(
                width="1px",
                height="28px",
                background=BORDER,
                margin_x="0.5rem",
            ),

            rx.center(
                rx.text(
                    "A",
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                    font_size=FONT_SIZE_SM,
                    color="white",
                ),
                width="36px",
                height="36px",
                border_radius="50%",
                background="#272361",
            ),

            rx.vstack(
                rx.text(
                    "Administrador",
                    color=TEXT_PRIMARY,
                    font_size=FONT_SIZE_SM,
                    font_weight=FONT_WEIGHT_MEDIUM,
                ),
                rx.text(
                    "Painel administrativo",
                    color=TEXT_SECONDARY,
                    font_size="0.72rem",
                ),
                spacing="0",
                align="start",
            ),

            rx.icon(
                tag="chevron_down",
                size=16,
                color=TEXT_SECONDARY,
            ),

            align="center",
            spacing="3",
        ),

        width="100%",
        height="72px",
        padding_x="1.75rem",
        background=HEADER_BACKGROUND,
        border_bottom=f"1px solid {BORDER}",
        align="center",
        flex_shrink="0",
    )