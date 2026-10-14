import reflex as rx

from Back_end.interface.state.meta.meta_detail_state import ( MetaDetailState,)
from Back_end.interface.theme.semantic import ( TEXT_PRIMARY, TEXT_PRIMARY_DARK, TEXT_SECONDARY, TEXT_SECONDARY_DARK,)
from Back_end.interface.theme.typography import ( FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY,)
BREADCRUMB_TEXT = rx.color_mode_cond( TEXT_PRIMARY, TEXT_PRIMARY_DARK,)
BREADCRUMB_MUTED = rx.color_mode_cond( TEXT_SECONDARY, TEXT_SECONDARY_DARK,)


def meta_breadcrumb() -> rx.Component:
    """
    Caminho de navegação da ficha da meta.

    Exemplo:
    METAS > META 001
    """

    return rx.hstack(
        rx.link(
            rx.text(
                "METAS",
                font_family=FONT_FAMILY_SECUNDARY,
                font_size="0.9rem",
                color="#2C7A45",
                cursor="pointer",
                _hover={
                    "text_decoration": "underline",
                },
            ),
            href="/admin/metas",
            text_decoration="none",
        ),

        rx.icon(
            tag="chevron-right",
            size=14,
            color=BREADCRUMB_MUTED,
        ),

        rx.text(
            "META ",
            MetaDetailState.codigo_atual,
            font_family=FONT_FAMILY_SECUNDARY,
            font_size="0.9rem",
            color=BREADCRUMB_TEXT,
        ),

        spacing="2",
        align="center",
        width="100%",
    )