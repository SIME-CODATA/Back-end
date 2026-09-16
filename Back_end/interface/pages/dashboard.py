import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.state.dashboard_state import DashboardState
from Back_end.interface.theme.semantic import (
    BORDER,
    SURFACE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from Back_end.interface.theme.typography import (
    FONT_SIZE_SM,
    FONT_SIZE_MD,
    FONT_SIZE_XL,
    FONT_SIZE_2XL,
    FONT_WEIGHT_BOLD,
    FONT_WEIGHT_MEDIUM,
    FONT_WEIGHT_SEMIBOLD,
)


def stat_card(
    title: str,
    value,
    description: str,
    icon: str,
    accent: str,
) -> rx.Component:
    """Card resumido utilizado no dashboard."""

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon(
                        tag=icon,
                        size=20,
                        color=accent,
                    ),
                    width="42px",
                    height="42px",
                    border_radius="10px",
                    background=f"color-mix(in srgb, {accent} 10%, transparent)",
                ),

                rx.spacer(),

                rx.icon(
                    tag="ellipsis",
                    size=18,
                    color=TEXT_SECONDARY,
                ),

                width="100%",
                align="center",
            ),

            rx.vstack(
                rx.text(
                    value,
                    color=TEXT_PRIMARY,
                    font_size=FONT_SIZE_2XL,
                    font_weight=FONT_WEIGHT_BOLD,
                ),
                rx.text(
                    title,
                    color=TEXT_PRIMARY,
                    font_size=FONT_SIZE_MD,
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                ),
                rx.text(
                    description,
                    color=TEXT_SECONDARY,
                    font_size=FONT_SIZE_SM,
                ),
                spacing="0",
                align="start",
            ),

            spacing="5",
            align="stretch",
            width="100%",
        ),

        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        padding="1.4rem",
        width="100%",
        min_height="175px",
        transition="transform 0.2s ease, box-shadow 0.2s ease",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 8px 24px rgba(39, 35, 97, 0.08)",
        },
    )


def dashboard_header() -> rx.Component:
    """Apresentação da página inicial."""

    return rx.hstack(
        rx.vstack(
            rx.text(
                "Visão Geral",
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_XL,
                font_weight=FONT_WEIGHT_BOLD,
            ),
            rx.text(
                "Acompanhe as principais informações do Programa de Metas.",
                color=TEXT_SECONDARY,
                font_size=FONT_SIZE_SM,
            ),
            spacing="1",
            align="start",
        ),

        rx.spacer(),

        rx.button(
            rx.icon( tag="refresh_cw", size=16,),

            rx.cond(
                DashboardState.loading, "Atualizando...", "Atualizar dados",),

                on_click=DashboardState.refresh_data,

                background="#272361",
                color="white",
                border_radius="8px",
                padding_x="1rem",
                cursor="pointer",

                disabled=DashboardState.loading,

                _hover={"background": "#124E8A",},
        ),

        width="100%",
        align="center",
    )


def dashboard_cards() -> rx.Component:
    """Indicadores principais do dashboard."""

    return rx.grid(
        stat_card(
            title="Metas",
            value=DashboardState.total_metas,
            description="Metas cadastradas no Programa de Metas",
            icon="target",
            accent="#03A8C5",
        ),

        stat_card(
            title="Eixos",
            value=DashboardState.total_temas,
            description="Eixos do Programa de Metas",
            icon="layers",
            accent="#124E8A",
        ),

        stat_card(
            title="Metas ativas",
            value=DashboardState.metas_ativas,
            description="Metas atualmente ativas",
            icon="circle_check",
            accent="#288140",
        ),

        stat_card(
            title="Última atualização",
            value=DashboardState.ultima_sincronizacao,
            description="Última sincronização com o SMAE",
            icon="refresh_cw",
            accent="#F7991C",
        ),

        columns={
            "initial": "1",
            "sm": "2",
            "lg": "4",
        },
        spacing="4",
        width="100%",
    )


def axis_item(axis) -> rx.Component:
    """Exibe um eixo e sua quantidade de metas."""

    return rx.hstack(
        rx.hstack(
            rx.box(
                width="10px",
                height="10px",
                border_radius="50%",
                background="#03A8C5",
                flex_shrink="0",
            ),

            rx.text(
                axis["nome"],
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_SM,
                font_weight=FONT_WEIGHT_MEDIUM,
            ),

            spacing="3",
            align="center",
        ),

        rx.spacer(),

        rx.box(
            rx.text(
                axis["quantidade"],
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_MD,
                font_weight=FONT_WEIGHT_BOLD,
            ),
            background="#F3F6F9",
            border_radius="8px",
            padding="0.35rem 0.75rem",
        ),

        width="100%",
        align="center",
        padding_y="0.65rem",
        border_bottom=f"1px solid {BORDER}",
    )


def dashboard_placeholder() -> rx.Component:
    """Área de informações detalhadas do dashboard."""

    return rx.grid(
        # Metas por eixo
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "Metas por eixo",
                            color=TEXT_PRIMARY,
                            font_size=FONT_SIZE_MD,
                            font_weight=FONT_WEIGHT_SEMIBOLD,
                        ),
                        rx.text(
                            "Distribuição das metas do Programa de Metas",
                            color=TEXT_SECONDARY,
                            font_size=FONT_SIZE_SM,
                        ),
                        spacing="0",
                        align="start",
                    ),

                    rx.spacer(),

                    rx.hstack(
                        rx.text(
                            DashboardState.total_temas,
                            color=TEXT_PRIMARY,
                            font_size=FONT_SIZE_MD,
                            font_weight=FONT_WEIGHT_BOLD,
                        ),
                        rx.text(
                            "eixos",
                            color=TEXT_SECONDARY,
                            font_size=FONT_SIZE_SM,
                        ),
                        spacing="1",
                        align="center",
                    ),

                    width="100%",
                    align="center",
                ),

                rx.vstack(
                    rx.foreach(
                        DashboardState.metas_por_eixo,
                        axis_item,
                    ),
                    width="100%",
                    spacing="0",
                    align="stretch",
                ),

                width="100%",
                align="stretch",
                spacing="4",
            ),

            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="12px",
            padding="1.5rem",
            width="100%",
        ),

        # Atividade recente
        rx.box(
            rx.vstack(
                rx.text(
                    "Atividade recente",
                    color=TEXT_PRIMARY,
                    font_size=FONT_SIZE_MD,
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                ),

                rx.center(
                    rx.vstack(
                        rx.icon(
                            tag="history",
                            size=32,
                            color=TEXT_SECONDARY,
                        ),
                        rx.text(
                            "Nenhuma atividade para exibir.",
                            color=TEXT_SECONDARY,
                            font_size=FONT_SIZE_SM,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    width="100%",
                    min_height="250px",
                ),

                width="100%",
                align="stretch",
            ),

            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="12px",
            padding="1.5rem",
            width="100%",
        ),

        columns={
            "initial": "1",
            "lg": "2fr 1fr",
        },
        spacing="4",
        width="100%",
    )


def dashboard_content() -> rx.Component:
    """Conteúdo da página inicial."""

    return rx.vstack(
        dashboard_header(),

        rx.cond(
            DashboardState.sync_message != "",
            rx.box(
                rx.text( DashboardState.sync_message, font_size=FONT_SIZE_SM, color="#288140",),
                width="100%",
                padding="0.65rem 0.9rem",
                background="rgba(40, 129, 64, 0.08)",
                border_radius="8px",
            ),
        ),

        rx.cond(
            DashboardState.error_message != "",
            rx.box(
                rx.text( DashboardState.error_message, font_size=FONT_SIZE_SM, color="#EC2024",),
                width="100%",
                padding="0.65rem 0.9rem",
                background="rgba(236, 32, 36, 0.08)",
                border_radius="8px",
            ),
        ),

        dashboard_cards(),
        dashboard_placeholder(),

        width="100%",
        spacing="6",
        align="stretch",
        on_mount=DashboardState.load_summary,
    )


def dashboard_page() -> rx.Component:
    """Página principal do painel administrativo."""

    return admin_layout(
        dashboard_content()
    )