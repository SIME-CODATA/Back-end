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
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_WEIGHT_SEMIBOLD,
)


# ============================================================
# CORES
# ============================================================

STATUS_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

STATUS_LABEL = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)


# ============================================================
# ITEM
# ============================================================

def status_item(
    label: str,
    value,
    icon: str,
) -> rx.Component:
    """Item reutilizável do bloco de status."""

    return rx.hstack(
        rx.center(
            rx.icon(
                tag=icon,
                size=17,
                color="#288140",
            ),

            width="34px",
            height="34px",
            min_width="34px",

            border_radius="10px",

            background=rx.color_mode_cond(
                "#EEF7F0",
                "rgba(40, 129, 64, 0.16)",
            ),
        ),

        rx.vstack(
            rx.text(
                label,
                color=STATUS_LABEL,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.72rem",
                font_weight="600",
            ),

            rx.text(
                value,
                color=STATUS_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.9rem",
                font_weight=FONT_WEIGHT_SEMIBOLD,
            ),

            spacing="1",
            align="start",
        ),

        spacing="3",
        align="center",
        width="100%",
    )


# ============================================================
# CARD
# ============================================================

def meta_status_card() -> rx.Component:
    """
    Exibe andamento, situação e prazo da meta.
    """

    return meta_section(
        "STATUS DA META",

        rx.grid(
            status_item(
                "Andamento",
                MetaDetailState.andamento,
                "chart-no-axes-column-increasing",
            ),

            status_item(
                "Situação",
                MetaDetailState.situacao,
                "circle-check",
            ),

            status_item(
                "Previsão",
                MetaDetailState.prazo,
                "calendar-days",
            ),

            columns={
                "initial": "1",
                "md": "3",
            },

            spacing="4",
            width="100%",
        ),
    )