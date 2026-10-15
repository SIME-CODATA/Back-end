import reflex as rx

from Back_end.interface.layouts.admin_layout import (
    admin_layout,
)

from Back_end.access.states.auth_state import (
    AuthState,
)

from Back_end.interface.theme.semantic import (
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)


PRIMARY_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

SECONDARY_TEXT = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)


def users_content() -> rx.Component:
    """Estrutura inicial da administração de usuários."""

    return rx.vstack(
        rx.text(
            "USUÁRIOS",

            color=PRIMARY_TEXT,

            font_family=FONT_FAMILY_SECUNDARY,

            font_size="2.4rem",

            line_height="1",
        ),

        rx.text(
            "Administração de usuários e permissões.",

            color=SECONDARY_TEXT,

            font_family=FONT_FAMILY_PRIMARY,

            font_size="0.9rem",
        ),

        rx.box(
            rx.vstack(
                rx.icon(
                    tag="users",
                    size=28,
                    color="#1287B2",
                ),

                rx.text(
                    "Controle de acesso funcionando",

                    color=PRIMARY_TEXT,

                    font_family=FONT_FAMILY_PRIMARY,

                    font_weight="600",
                ),

                rx.text(
                    "Perfil atual: ",
                    AuthState.current_role_label,

                    color=SECONDARY_TEXT,

                    font_family=FONT_FAMILY_PRIMARY,

                    font_size="0.85rem",
                ),

                spacing="3",
                align="center",
            ),

            width="100%",

            padding="3rem",

            border=rx.color_mode_cond(
                "1px solid #E0E5EC",
                "1px solid rgba(255,255,255,0.12)",
            ),

            border_radius="12px",
        ),

        width="100%",

        spacing="5",

        align="stretch",
    )


def users_page() -> rx.Component:
    """Página administrativa de usuários."""

    return admin_layout(
        users_content()
    )