import reflex as rx

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)


# ============================================================
# SEÇÃO
# ============================================================

def meta_print_section(
    title: str,
    *children,
    allow_break: bool = False,
) -> rx.Component:
    """
    Seção reutilizável do documento.

    allow_break=True permite que seções grandes,
    como Obras, continuem na próxima página.
    """

    class_name = (
        "print-section print-allow-break"
        if allow_break
        else "print-section"
    )

    return rx.box(
        rx.vstack(
            rx.text(
                title,
                color="#17213C",
                font_family=(
                    FONT_FAMILY_SECUNDARY
                ),
                font_size="1.05rem",
                line_height="1",
            ),

            rx.box(
                width="100%",
                height="2px",
                background="#288140",
            ),

            *children,

            spacing="3",
            align="stretch",
            width="100%",
        ),

        class_name=class_name,

        width="100%",

        padding="0.85rem",

        border="1px solid #D8DEE8",

        border_radius="10px",

        background="#FFFFFF",
    )


# ============================================================
# CAMPO
# ============================================================

def meta_print_info(
    label: str,
    value,
) -> rx.Component:
    """Campo textual compacto do documento."""

    return rx.vstack(
        rx.text(
            label,
            color="#667085",
            font_family=FONT_FAMILY_PRIMARY,
            font_size="0.64rem",
            font_weight="600",
            line_height="1",
        ),

        rx.text(
            value,
            color="#17213C",
            font_family=FONT_FAMILY_PRIMARY,
            font_size="0.78rem",
            font_weight="600",
            line_height="1.35",
        ),

        spacing="1",
        align="start",
        width="100%",
    )


# ============================================================
# CHIP
# ============================================================

def meta_print_chip(
    value,
) -> rx.Component:
    """Chip usado nas informações categóricas."""

    return rx.box(
        rx.text(
            value,
            color="#17213C",
            font_family=FONT_FAMILY_PRIMARY,
            font_size="0.68rem",
            line_height="1.2",
        ),

        padding="0.28rem 0.5rem",

        background="#F0F3F6",

        border_radius="999px",

        width="fit-content",
    )