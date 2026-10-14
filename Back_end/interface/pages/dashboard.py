import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.state.dashboard_state import DashboardState
from Back_end.interface.theme.semantic import ( BORDER, SURFACE, TEXT_PRIMARY, TEXT_SECONDARY,COLOR_UNIVERSO, COLOR_VIVER, COLOR_CIDADE, COLOR_CAPITAL, COLOR_TOTAL)
from Back_end.interface.theme.typography import ( FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_XL, FONT_WEIGHT_BOLD, FONT_WEIGHT_MEDIUM, FONT_WEIGHT_SEMIBOLD,)

from Back_end.interface.components.graphics.meta_distribution_chart import ( meta_distribution_chart,)
from Back_end.interface.components.graphics.budget_donut_chart import ( budget_donut_chart,)


# ============================================================
# CORES DO PDM
# ============================================================
COLOR_HEADER = rx.color_mode_cond ("#2C286D", "#0056ab")

COLOR_GREEN = "#288140"
COLOR_CYAN = "#03A8C5"
COLOR_ORANGE = "#F7991C"
COLOR_RED = "#EC2024"

PANEL_BORDER = "#364237"


# ============================================================
# CABEÇALHO
# ============================================================

def dashboard_header() -> rx.Component:
    """Cabeçalho da página."""
    return rx.vstack(
        rx.box(
            rx.center(
                rx.text(
                    "PANORAMA GERAL DO BALANÇO DO PDM 25/28",
                    color="white",
                    font_size={ "initial": "1.45rem", "md": "2rem", "lg": "2.6rem",},
                    font_weight=FONT_WEIGHT_BOLD,
                    text_align="center",
                    ),
    
                min_height="128px",
                width="100%",
                position="relative",
                bottom="1.5rem",
            ),
    
            background=COLOR_HEADER,
            width="100%",
            border_top_right_radius="20px",
        ),
    
        rx.grid(
            rx.foreach(
                DashboardState.eixos_resumo,
                panorama_axis_card,
            ),
    
            panorama_total_card(),

            columns={
                "initial": "1",
                "sm": "2",
                "lg": "5",
            },

            spacing="4",
            width="100%",
            position="relative",
            bottom="3rem",
        ),
    
        width="100%",
        spacing="0",
        align="stretch",
    )


# ============================================================
# PANORAMA GERAL
# ============================================================

def axis_color(axis) -> rx.Var:
    """Retorna a cor institucional de cada eixo."""

    return rx.cond(
        axis["nome"] == "Universo SP",
        COLOR_UNIVERSO,
        rx.cond(
            axis["nome"] == "Viver São Paulo",
            COLOR_VIVER,
            rx.cond(
                axis["nome"] == "Cidade Empreendedora",
                COLOR_CIDADE,
                COLOR_CAPITAL,
            ),
        ),
    )


def panorama_axis_card(axis) -> rx.Component:
    """Card individual de um eixo."""

    color = axis_color(axis)

    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        axis["quantidade"],
                        color="white",
                        font_size="2rem",
                        font_weight=FONT_WEIGHT_BOLD,
                        line_height="1",
                    ),

                    rx.text(
                        "METAS",
                        color="white",
                        font_size="0.7rem",
                        font_weight=FONT_WEIGHT_BOLD,
                    ),

                    spacing="1",
                    align="end",
                ),

                rx.text(
                    axis["nome"],
                    color="white",
                    font_size="0.78rem",
                    font_weight=FONT_WEIGHT_BOLD,
                    text_transform="uppercase",
                ),

                spacing="2",
                align="center",
                justify="center",
                width="100%",
            ),

            background=color,
            width="100%",
            min_height="75px",
            display="flex",
            align_items="center",
            justify_content="center",
            position="relative",
            botton="2rem",

            border_top_right_radius="20px",
        ),

        rx.box(
            rx.hstack(
                rx.text(
                    axis["atingidas"],
                    color="white",
                    font_size="1.25rem",
                    font_weight=FONT_WEIGHT_BOLD,
                ),

                rx.text(
                    "ATINGIDAS",
                    color="white",
                    font_size="0.72rem",
                    font_weight=FONT_WEIGHT_BOLD,
                ),

                spacing="2",
                align="center",
                justify="center",
            ),

            background=color,
            width="100%",
            padding="0.9rem",
        ),

        spacing="2",
        width="100%",
    )


def panorama_total_card() -> rx.Component:
    """Card com o total do PDM."""

    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        DashboardState.total_metas,
                        color="white",
                        font_size="2rem",
                        font_weight=FONT_WEIGHT_BOLD,
                        line_height="1",
                    ),

                    rx.text(
                        "METAS",
                        color="white",
                        font_size="0.7rem",
                        font_weight=FONT_WEIGHT_BOLD,
                    ),

                    spacing="1",
                    align="end",
                ),

                rx.text(
                    "TOTAL",
                    color="white",
                    font_size="0.78rem",
                    font_weight=FONT_WEIGHT_BOLD,
                ),

                spacing="2",
                align="center",
                justify="center",
                width="100%",
            ),

            background=COLOR_TOTAL,
            width="100%",
            min_height="75px",
            display="flex",
            align_items="center",
            justify_content="center",

            border_top_left_radius="20px",
        ),

        rx.box(
            rx.hstack(
                rx.text(
                    DashboardState.metas_atingidas,
                    color="white",
                    font_size="1.25rem",
                    font_weight=FONT_WEIGHT_BOLD,
                ),

                rx.text(
                    "ATINGIDAS",
                    color="white",
                    font_size="0.72rem",
                    font_weight=FONT_WEIGHT_BOLD,
                ),

                spacing="2",
                align="center",
                justify="center",
            ),

            background=COLOR_TOTAL,
            width="100%",
            padding="0.9rem",
        ),

        spacing="2",
        width="100%",
    )

# ============================================================
# CONTEÚDO
# ============================================================

def dashboard_content() -> rx.Component:
    """Conteúdo principal do dashboard."""

    return rx.vstack(
        dashboard_header(),
        rx.grid(
            meta_distribution_chart(
                figure=DashboardState.meta_distribution_figure,
                situacao=DashboardState.situacao_resumo,
                prazos=DashboardState.prazo_resumo,
            ),
            
            budget_donut_chart(
                figure=DashboardState.budget_figure,
            ),

            columns={
                "initial": "1",
                "lg": "2fr 1fr",
            },

            spacing="3",
            width="100%",
            align_items="stretch",
        ),

        width="100%",
        spacing="5",
        align="stretch",
        padding_bottom="2rem",
    )

def dashboard_page() -> rx.Component:
    """Página principal do painel administrativo."""

    return admin_layout(
        dashboard_content()
    )