import reflex as rx

from Back_end.interface.theme.semantic import ( BORDER, BORDER_DARK, SURFACE, SURFACE_DARK, TEXT_PRIMARY, TEXT_PRIMARY_DARK,)
from Back_end.interface.theme.typography import ( FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY,)

SECTION_BACKGROUND = rx.color_mode_cond( SURFACE, SURFACE_DARK,)
SECTION_BORDER = rx.color_mode_cond( BORDER, BORDER_DARK,)
SECTION_TEXT = rx.color_mode_cond( TEXT_PRIMARY, TEXT_PRIMARY_DARK,)


def meta_section( title: str, *children, width: str = "100%", min_height: str | None = None, ) -> rx.Component:
    """
    Bloco visual reutilizável da Ficha da Meta.
    """

    return rx.box(
        rx.vstack(
            rx.text(
                title,
                color=SECTION_TEXT,
                font_family=FONT_FAMILY_SECUNDARY,
                font_size="1.15rem",
                line_height="1",
            ),

            *children,

            spacing="4",
            align="stretch",
            width="100%",
        ),

        width=width,
        min_height=min_height,
        background=SECTION_BACKGROUND,
        border=f"1px solid {SECTION_BORDER}",
        border_radius="18px",
        padding="1rem",
    )