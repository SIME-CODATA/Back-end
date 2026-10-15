import reflex as rx

from Back_end.interface.components.meta.detail.meta_section import (
    meta_section,
)

from Back_end.interface.state.meta.meta_detail_state import (
    MetaDetailState,
)

from Back_end.interface.theme.semantic import (
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
    BORDER,
    BORDER_DARK,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_WEIGHT_SEMIBOLD,
)


# ============================================================
# CORES
# ============================================================

INITIATIVE_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

INITIATIVE_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

INITIATIVE_BORDER = rx.color_mode_cond(
    BORDER,
    BORDER_DARK,
)

INITIATIVE_BACKGROUND = rx.color_mode_cond(
    "#F8FAFB",
    "rgba(255, 255, 255, 0.04)",
)


# ============================================================
# ITEM
# ============================================================

def initiative_item(
    value,
) -> rx.Component:
    """Card individual de uma iniciativa."""

    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(
                    tag="milestone",
                    size=16,
                    color="#288140",
                ),

                width="34px",
                height="34px",
                min_width="34px",

                border_radius="10px",

                background=rx.color_mode_cond(
                    "#EAF5ED",
                    "rgba(40, 129, 64, 0.14)",
                ),
            ),

            rx.text(
                value,
                color=INITIATIVE_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.84rem",
                font_weight=FONT_WEIGHT_SEMIBOLD,
                line_height="1.4",
            ),

            spacing="3",
            align="start",
        ),

        width="100%",

        padding="0.9rem",

        background=INITIATIVE_BACKGROUND,

        border=f"1px solid {INITIATIVE_BORDER}",

        border_radius="12px",
    )


# ============================================================
# CARD
# ============================================================

def meta_initiatives_card() -> rx.Component:
    """Exibe as iniciativas cadastradas para a meta."""

    return meta_section(
        "INICIATIVAS",

        rx.cond(
            MetaDetailState.iniciativas.length() > 0,

            rx.grid(
                rx.foreach(
                    MetaDetailState.iniciativas,
                    initiative_item,
                ),

                columns={
                    "initial": "1",
                    "lg": "2",
                },

                spacing="3",
                padding="1rem",
                width="100%",
            ),

            rx.vstack(
                rx.icon(
                    tag="circle-slash",
                    size=18,
                    color=INITIATIVE_MUTED,
                ),

                rx.text(
                    "Nenhuma iniciativa cadastrada "
                    "para esta meta.",
                    color=INITIATIVE_MUTED,
                    font_family=FONT_FAMILY_PRIMARY,
                    font_size="0.84rem",
                ),

                spacing="2",
                align="center",
                width="100%",
                padding="1rem",
            ),
        ),
    )