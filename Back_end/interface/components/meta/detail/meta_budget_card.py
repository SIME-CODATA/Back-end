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

BUDGET_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

BUDGET_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

BUDGET_BACKGROUND = rx.color_mode_cond(
    "#F6F8FA",
    "rgba(255, 255, 255, 0.05)",
)


# ============================================================
# ITEM
# ============================================================

def budget_item(
    label: str,
    value,
    icon: str,
) -> rx.Component:
    """Item individual do orçamento."""

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon(
                        tag=icon,
                        size=16,
                        color="#288140",
                    ),

                    width="32px",
                    height="32px",

                    border_radius="9px",

                    background=rx.color_mode_cond(
                        "#EAF5ED",
                        "rgba(40, 129, 64, 0.14)",
                    ),
                ),

                rx.text(
                    label,
                    color=BUDGET_MUTED,
                    font_family=FONT_FAMILY_PRIMARY,
                    font_size="0.75rem",
                    font_weight="600",
                ),

                spacing="2",
                align="center",
            ),

            rx.text(
                value,
                color=BUDGET_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size={
                    "initial": "1rem",
                    "md": "1.08rem",
                },
                font_weight=FONT_WEIGHT_SEMIBOLD,
            ),

            spacing="3",
            align="start",
        ),

        width="100%",

        padding="1rem",

        background=BUDGET_BACKGROUND,

        border_radius="12px",
    )


# ============================================================
# CARD
# ============================================================

def meta_budget_card() -> rx.Component:
    """Exibe os dados orçamentários da meta."""

    return meta_section(
        "ORÇAMENTO",

        rx.grid(
            budget_item(
                "Recursos previstos",
                MetaDetailState.previsao,
                "wallet-cards",
            ),

            budget_item(
                "Empenhado",
                MetaDetailState.empenhado,
                "file-check-2",
            ),

            budget_item(
                "Liquidado",
                MetaDetailState.liquidado,
                "circle-dollar-sign",
            ),

            columns={
                "initial": "1",
                "md": "3",
            },
            padding="1rem",

            spacing="4",
            width="100%",
        ),
    )