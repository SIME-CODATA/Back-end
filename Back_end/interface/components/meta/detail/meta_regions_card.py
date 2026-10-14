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

REGION_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

REGION_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

REGION_CHIP_BACKGROUND = rx.color_mode_cond(
    "#EEF7F0",
    "rgba(40, 129, 64, 0.16)",
)

SUBPREF_CHIP_BACKGROUND = rx.color_mode_cond(
    "#F4F6F8",
    "rgba(255, 255, 255, 0.07)",
)


# ============================================================
# CHIP DE REGIÃO
# ============================================================

def region_chip(
    value,
) -> rx.Component:
    """Chip de uma região relacionada à meta."""

    return rx.box(
        rx.hstack(
            rx.icon(
                tag="map-pin",
                size=13,
                color="#288140",
            ),

            rx.text(
                value,
                color=REGION_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.78rem",
                font_weight=FONT_WEIGHT_SEMIBOLD,
            ),

            spacing="2",
            align="center",
        ),

        padding="0.4rem 0.65rem",

        background=REGION_CHIP_BACKGROUND,

        border_radius="999px",

        width="fit-content",
    )


# ============================================================
# CHIP DE SUBPREFEITURA
# ============================================================

def subprefeitura_chip(
    value,
) -> rx.Component:
    """Chip de uma subprefeitura relacionada à meta."""

    return rx.box(
        rx.text(
            value,
            color=REGION_TEXT,
            font_family=FONT_FAMILY_PRIMARY,
            font_size="0.76rem",
        ),

        padding="0.35rem 0.6rem",

        background=SUBPREF_CHIP_BACKGROUND,

        border_radius="8px",

        width="fit-content",
    )


# ============================================================
# CARD
# ============================================================

def meta_regions_card() -> rx.Component:
    """
    Exibe a cobertura territorial identificada
    a partir das obras relacionadas à meta.
    """

    return meta_section(
        "REGIONALIZAÇÃO",

        rx.grid(

            # =================================================
            # REGIÕES
            # =================================================

            rx.vstack(
                rx.hstack(
                    rx.icon(
                        tag="map",
                        size=15,
                        color="#288140",
                    ),

                    rx.text(
                        "Regiões com obras relacionadas",
                        color=REGION_MUTED,
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.78rem",
                        font_weight="600",
                    ),

                    spacing="2",
                    align="center",
                ),

                rx.cond(
                    MetaDetailState.regioes.length() > 0,

                    rx.flex(
                        rx.foreach(
                            MetaDetailState.regioes,
                            region_chip,
                        ),

                        wrap="wrap",
                        gap="0.5rem",
                        width="100%",
                    ),

                    rx.text(
                        "Nenhuma região identificada "
                        "nas obras relacionadas.",
                        color=REGION_MUTED,
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.82rem",
                    ),
                ),

                spacing="3",
                align="start",
                width="100%",
            ),

            # =================================================
            # SUBPREFEITURAS
            # =================================================

            rx.vstack(
                rx.hstack(
                    rx.icon(
                        tag="landmark",
                        size=15,
                        color="#288140",
                    ),

                    rx.text(
                        "Subprefeituras",
                        color=REGION_MUTED,
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.78rem",
                        font_weight="600",
                    ),

                    spacing="2",
                    align="center",
                ),

                rx.cond(
                    MetaDetailState
                    .subprefeituras
                    .length()
                    > 0,

                    rx.flex(
                        rx.foreach(
                            MetaDetailState.subprefeituras,
                            subprefeitura_chip,
                        ),

                        wrap="wrap",
                        gap="0.45rem",
                        width="100%",
                    ),

                    rx.text(
                        "Nenhuma subprefeitura identificada.",
                        color=REGION_MUTED,
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.82rem",
                    ),
                ),

                spacing="3",
                align="start",
                width="100%",
            ),

            columns={
                "initial": "1",
                "lg": "2",
            },

            spacing="5",
            width="100%",
        ),
    )