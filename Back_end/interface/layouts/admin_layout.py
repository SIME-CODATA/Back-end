import reflex as rx

from Back_end.interface.components.header import header
from Back_end.interface.components.sidebar import sidebar
from Back_end.interface.theme.semantic import PAGE_BACKGROUND
from Back_end.interface.theme.typography import FONT_FAMILY_PRIMARY


def admin_layout(content: rx.Component) -> rx.Component:
    """Layout principal das páginas administrativas."""

    return rx.hstack(
        # Navegação lateral
        sidebar(),

        # Área principal
        rx.vstack(
            header(),

            rx.box(
                content,
                width="100%",
                flex="1",
                padding="2rem",
                overflow_y="auto",
            ),

            width="100%",
            height="100vh",
            spacing="0",
            align="stretch",
            overflow="hidden",
        ),

        width="100%",
        height="100vh",
        spacing="0",
        align="stretch",
        background=PAGE_BACKGROUND,
        font_family=FONT_FAMILY_PRIMARY,
        overflow="hidden",
    )