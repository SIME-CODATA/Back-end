import reflex as rx

from Back_end.interface.components.meta.detail.meta_section import (
    meta_section,
)

from Back_end.interface.state.meta.meta_detail_state import (
    MetaDetailState,
    MetaProjetoItem,
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

PROJECT_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

PROJECT_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

PROJECT_BORDER = rx.color_mode_cond(
    BORDER,
    BORDER_DARK,
)

PROJECT_BACKGROUND = rx.color_mode_cond(
    "#F8FAFB",
    "rgba(255, 255, 255, 0.04)",
)

PROJECT_INFO_BACKGROUND = rx.color_mode_cond(
    "#FFFFFF",
    "rgba(255, 255, 255, 0.05)",
)


# ============================================================
# INFORMAÇÃO
# ============================================================

def project_info(
    label: str,
    value,
    icon: str,
) -> rx.Component:
    """Informação compacta de um projeto."""

    return rx.hstack(
        rx.icon(
            tag=icon,
            size=13,
            color="#00aaff",
        ),

        rx.vstack(
            rx.text(
                label,
                color=PROJECT_MUTED,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.65rem",
                font_weight="600",
                line_height="1",
            ),

            rx.text(
                value,
                color=PROJECT_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.74rem",
                line_height="1.25",
            ),

            spacing="1",
            align="start",
            min_width="0",
        ),

        spacing="2",
        align="start",

        padding="0.5rem",

        background=PROJECT_INFO_BACKGROUND,

        border_radius="8px",

        width="100%",
        min_width="0",
    )


# ============================================================
# PROJETO
# ============================================================

def project_item(
    projeto: rx.Var[MetaProjetoItem],
) -> rx.Component:
    """Card compacto de um projeto relacionado."""

    return rx.box(
        rx.vstack(

            # ------------------------------------------------
            # Código
            # ------------------------------------------------

            rx.text(
                projeto["codigo"],
                color="#00aaff",
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.68rem",
                font_weight="700",
            ),

            # ------------------------------------------------
            # Nome
            # ------------------------------------------------

            rx.text(
                projeto["nome"],
                color=PROJECT_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.86rem",
                font_weight=FONT_WEIGHT_SEMIBOLD,
                line_height="1.3",
            ),

            # ------------------------------------------------
            # Informações
            # ------------------------------------------------

            rx.grid(
                project_info(
                    "Portfólio",
                    projeto["portfolio"],
                    "folder-kanban",
                ),

                project_info(
                    "Etapa",
                    projeto["etapa"],
                    "workflow",
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

        background=PROJECT_BACKGROUND,

        border=f"1px solid {PROJECT_BORDER}",

        border_radius="12px",

        transition=(
            "border-color 0.2s ease, "
            "transform 0.2s ease"
        ),

        _hover={
            "border_color": "#00aaff",
            "transform": "translateY(-1px)",
        },
    )


# ============================================================
# COMPONENTE PRINCIPAL
# ============================================================

def meta_projects_card() -> rx.Component:
    """Exibe os projetos relacionados à meta."""

    return meta_section(
        "PROJETOS RELACIONADOS",

        rx.hstack(
            rx.icon(
                tag="folder-kanban",
                size=15,
                color="#00aaff",
            ),

            rx.text(
                MetaDetailState.projetos.length(),
                " projeto(s) encontrado(s)",
                color=PROJECT_MUTED,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.76rem",
            ),

            spacing="2",
            align="center",
        ),

        rx.cond(
            MetaDetailState.projetos.length() > 0,

            rx.grid(
                rx.foreach(
                    MetaDetailState.projetos,
                    project_item,
                ),

                columns={
                    "initial": "1",
                    "lg": "2",
                    "2xl": "3",
                },

                spacing="3",
                width="100%",
                padding="1rem",
                align_items="stretch",
            ),

            rx.center(
                rx.vstack(
                    rx.icon(
                        tag="folder-x",
                        size=22,
                        color=PROJECT_MUTED,
                    ),

                    rx.text(
                        "Nenhum projeto relacionado "
                        "a esta meta.",
                        color=PROJECT_MUTED,
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