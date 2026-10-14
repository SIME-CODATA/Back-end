import reflex as rx

from Back_end.interface.components.meta.detail.meta_section import (
    meta_section,
)

from Back_end.interface.state.meta.meta_detail_state import (
    MetaDetailState,
    MetaObraItem,
)

from Back_end.interface.theme.semantic import (
    BORDER,
    BORDER_DARK,
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

WORK_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

WORK_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

WORK_BORDER = rx.color_mode_cond(
    BORDER,
    BORDER_DARK,
)

WORK_BACKGROUND = rx.color_mode_cond(
    "#F8FAFB",
    "rgba(255, 255, 255, 0.04)",
)

WORK_INFO_BACKGROUND = rx.color_mode_cond(
    "#FFFFFF",
    "rgba(255, 255, 255, 0.05)",
)


# ============================================================
# INFORMAÇÃO COMPACTA
# ============================================================

def work_info(
    label: str,
    value,
    icon: str,
) -> rx.Component:
    """Informação resumida de uma obra."""

    return rx.hstack(
        rx.icon(
            tag=icon,
            size=13,
            color="#288140",
        ),

        rx.vstack(
            rx.text(
                label,
                color=WORK_MUTED,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.65rem",
                font_weight="600",
                line_height="1",
            ),

            rx.text(
                value,
                color=WORK_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.74rem",
                font_weight="500",
                line_height="1.2",
            ),

            spacing="1",
            align="start",
            min_width="0",
        ),

        spacing="2",
        align="start",

        padding="0.5rem",

        background=WORK_INFO_BACKGROUND,

        border_radius="8px",

        width="100%",
        min_width="0",
    )


# ============================================================
# OBRA
# ============================================================

def work_item(
    obra: rx.Var[MetaObraItem],
) -> rx.Component:
    """Card compacto de uma obra relacionada."""

    return rx.box(
        rx.vstack(

            # =================================================
            # CABEÇALHO
            # =================================================

            rx.hstack(
                rx.vstack(
                    rx.text(
                        obra["codigo"],
                        color="#288140",
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.68rem",
                        font_weight="700",
                    ),

                    rx.text(
                        obra["nome"],
                        color=WORK_TEXT,
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.86rem",
                        font_weight=FONT_WEIGHT_SEMIBOLD,
                        line_height="1.25",
                    ),

                    spacing="1",
                    align="start",
                    min_width="0",
                    flex="1",
                ),

                # ---------------------------------------------
                # Percentual
                # ---------------------------------------------

                rx.center(
                    rx.text(
                        obra["percentual"],
                        color="#288140",
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.74rem",
                        font_weight="700",
                    ),

                    min_width="48px",
                    height="30px",

                    padding_x="0.45rem",

                    background=rx.color_mode_cond(
                        "#EAF5ED",
                        "rgba(40, 129, 64, 0.15)",
                    ),

                    border_radius="999px",
                ),

                align="start",
                spacing="3",
                width="100%",
            ),

            # =================================================
            # STATUS
            # =================================================

            rx.hstack(
                rx.icon(
                    tag="circle-check",
                    size=13,
                    color="#288140",
                ),

                rx.text(
                    obra["status"],
                    color=WORK_MUTED,
                    font_family=FONT_FAMILY_PRIMARY,
                    font_size="0.7rem",
                    font_weight="600",
                ),

                spacing="2",
                align="center",

                width="fit-content",

                padding="0.3rem 0.55rem",

                background=rx.color_mode_cond(
                    "#EEF7F0",
                    "rgba(40, 129, 64, 0.12)",
                ),

                border_radius="999px",
            ),

            # =================================================
            # DETALHES
            # =================================================

            rx.grid(
                work_info(
                    "Tipo",
                    obra["tipo"],
                    "construction",
                ),

                work_info(
                    "Equipamento",
                    obra["equipamento"],
                    "building-2",
                ),

                work_info(
                    "Subprefeitura",
                    obra["subprefeituras"],
                    "map-pin",
                ),

                work_info(
                    "Conclusão",
                    obra["percentual"],
                    "chart-no-axes-column-increasing",
                ),

                columns={
                    "initial": "1",
                    "md": "2",
                },

                spacing="2",
                width="100%",
            ),

            spacing="3",
            align="stretch",
            width="100%",
        ),

        width="100%",
        height="100%",

        padding="0.9rem",

        background=WORK_BACKGROUND,

        border=f"1px solid {WORK_BORDER}",

        border_radius="12px",

        transition=(
            "border-color 0.2s ease, "
            "transform 0.2s ease"
        ),

        _hover={
            "border_color": "#288140",
            "transform": "translateY(-1px)",
        },
    )


# ============================================================
# COMPONENTE PRINCIPAL
# ============================================================

def meta_works_card() -> rx.Component:
    """
    Exibe todas as obras relacionadas à meta.

    As obras são organizadas em grid para manter
    a ficha compacta mesmo quando houver muitos registros.
    """

    return meta_section(
        "OBRAS RELACIONADAS",

        rx.hstack(
            rx.icon(
                tag="construction",
                size=15,
                color="#288140",
            ),

            rx.text(
                MetaDetailState.obras.length(),
                " obra(s) encontrada(s)",
                color=WORK_MUTED,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.76rem",
            ),

            spacing="2",
            align="center",
        ),

        rx.cond(
            MetaDetailState.obras.length() > 0,

            rx.grid(
                rx.foreach(
                    MetaDetailState.obras,
                    work_item,
                ),

                columns={
                    "initial": "1",
                    "lg": "2",
                    "2xl": "3",
                },

                spacing="3",
                width="100%",
                align_items="stretch",
            ),

            rx.center(
                rx.vstack(
                    rx.icon(
                        tag="construction",
                        size=22,
                        color=WORK_MUTED,
                    ),

                    rx.text(
                        "Nenhuma obra relacionada "
                        "a esta meta.",
                        color=WORK_MUTED,
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.82rem",
                    ),

                    spacing="2",
                    align="center",
                ),

                width="100%",
                padding="1.5rem",
            ),
        ),
    )