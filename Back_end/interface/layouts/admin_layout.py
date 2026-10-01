import reflex as rx

from Back_end.interface.components.header import header
from Back_end.interface.components.sidebar import sidebar
from Back_end.interface.theme.semantic import ( PAGE_BACKGROUND_GRADIENT, PAGE_BACKGROUND_GRADIENT_DARK,PAGE_BACKGROUND, PAGE_BACKGROUND_DARK)
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
            height="96vh",
            margin="1rem",
            spacing="0",
            align="stretch",
            overflow="hidden",
            box_shadow="3px 3px 13px -10px rgba(255, 255, 255, 0.65)",
            background=rx.color_mode_cond( PAGE_BACKGROUND, PAGE_BACKGROUND_DARK ),
            border_radius="15px",
        ),

        width="100%",
        height="100vh",
        spacing="0",
        align="stretch",
        background=rx.color_mode_cond( PAGE_BACKGROUND_GRADIENT, PAGE_BACKGROUND_GRADIENT_DARK,),
        font_family=FONT_FAMILY_PRIMARY,
        overflow="hidden",
        transition="filter 0.2s ease",
    )