import reflex as rx

from Back_end.interface.theme.semantic import (
    PAGE_BACKGROUND,
    PAGE_BACKGROUND_DARK,
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)


BACKGROUND = rx.color_mode_cond(
    PAGE_BACKGROUND,
    PAGE_BACKGROUND_DARK,
)

PRIMARY_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

SECONDARY_TEXT = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)


def forbidden_page() -> rx.Component:
    """Página exibida quando o usuário não possui permissão."""

    return rx.center(
        rx.vstack(
            rx.center(
                rx.icon(
                    tag="shield_alert",
                    size=36,
                    color="#EC2024",
                ),

                width="72px",
                height="72px",

                border_radius="50%",

                background=(
                    "rgba(236, 32, 36, 0.10)"
                ),
            ),

            rx.text(
                "403",

                font_family=FONT_FAMILY_SECUNDARY,

                font_size="4rem",

                line_height="1",

                color=PRIMARY_TEXT,
            ),

            rx.text(
                "ACESSO NÃO AUTORIZADO",

                font_family=FONT_FAMILY_SECUNDARY,

                font_size="1.5rem",

                color=PRIMARY_TEXT,

                text_align="center",
            ),

            rx.text(
                "Seu perfil não possui permissão "
                "para acessar esta área do sistema.",

                font_family=FONT_FAMILY_PRIMARY,

                font_size="0.9rem",

                color=SECONDARY_TEXT,

                text_align="center",

                max_width="420px",
            ),

            rx.link(
                rx.button(
                    rx.icon(
                        tag="arrow_left",
                        size=16,
                    ),

                    "Voltar ao painel",

                    cursor="pointer",
                ),

                href="/admin",

                text_decoration="none",
            ),

            spacing="4",

            align="center",
        ),

        width="100%",
        min_height="100vh",

        padding="2rem",

        background=BACKGROUND,

        font_family=FONT_FAMILY_PRIMARY,
    )