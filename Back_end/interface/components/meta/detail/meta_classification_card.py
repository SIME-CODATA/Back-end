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

CLASSIFICATION_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

CLASSIFICATION_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

CHIP_BACKGROUND = rx.color_mode_cond(
    "#F1F5F4",
    "rgba(255, 255, 255, 0.08)",
)


# ============================================================
# CHIP
# ============================================================

def classification_chip(
    value,
) -> rx.Component:
    """Chip reutilizável para órgãos e classificações."""

    return rx.box(
        rx.text(
            value,
            color=CLASSIFICATION_TEXT,
            font_family=FONT_FAMILY_PRIMARY,
            font_size="0.78rem",
            font_weight=FONT_WEIGHT_SEMIBOLD,
        ),

        background=CHIP_BACKGROUND,

        padding="0.4rem 0.65rem",

        border_radius="999px",

        width="fit-content",
    )


# ============================================================
# GRUPO
# ============================================================

def classification_group(
    title: str,
    icon: str,
    values,
    empty_text: str,
) -> rx.Component:
    """Grupo de informações da classificação."""

    return rx.vstack(
        rx.hstack(
            rx.icon(
                tag=icon,
                size=15,
                color="#288140",
            ),

            rx.text(
                title,
                color=CLASSIFICATION_MUTED,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.78rem",
                font_weight="600",
            ),

            spacing="2",
            align="center",
        ),

        rx.cond(
            values.length() > 0,

            rx.flex(
                rx.foreach(
                    values,
                    classification_chip,
                ),

                wrap="wrap",
                gap="0.5rem",
                width="100%",
            ),

            rx.text(
                empty_text,
                color=CLASSIFICATION_MUTED,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.82rem",
            ),
        ),

        spacing="3",
        align="start",
        width="100%",
    )


# ============================================================
# CARD
# ============================================================

def meta_classification_card() -> rx.Component:
    """
    Exibe órgãos vinculados e ODS da meta.
    """

    return meta_section(
        "CLASSIFICAÇÕES",

        rx.grid(
            classification_group(
                title="Órgãos vinculados",
                icon="building-2",
                values=MetaDetailState.orgaos,
                empty_text="Nenhum órgão informado.",
            ),

            classification_group(
                title="Objetivos de Desenvolvimento Sustentável",
                icon="leaf",
                values=MetaDetailState.ods,
                empty_text="Nenhum ODS informado.",
            ),

            columns={
                "initial": "1",
                "lg": "2",
            },

            spacing="5",
            padding="1rem",
            width="100%",
        ),
    )