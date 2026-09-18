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


# ============================================================
# CORES DO PDM
# ============================================================

COLOR_UNIVERSO = "#3ABB4B"
COLOR_VIVER = "#FF641E"
COLOR_CIDADE = "#1400C8"
COLOR_CAPITAL = "#87314F"
COLOR_TOTAL = "#1287B2"

COLOR_HEADER = "#2C286D"

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

    return rx.hstack(
        rx.vstack(
            rx.text(
                "Visão Geral",
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_XL,
                font_weight=FONT_WEIGHT_BOLD,
            ),
            rx.text(
                "Acompanhamento executivo do Programa de Metas 2025–2028.",
                color=TEXT_SECONDARY,
                font_size=FONT_SIZE_SM,
            ),
            spacing="1",
            align="start",
        ),

        rx.spacer(),

        rx.vstack(
            rx.text(
                "Última atualização",
                color=TEXT_SECONDARY,
                font_size="0.7rem",
                font_weight=FONT_WEIGHT_SEMIBOLD,
                text_transform="uppercase",
            ),

            rx.text(
                DashboardState.ultima_sincronizacao,
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_SM,
                font_weight=FONT_WEIGHT_SEMIBOLD,
            ),

            spacing="0",
            align="end",
        ),

        rx.button(
            rx.icon(
                tag="refresh_cw",
                size=15,
            ),

            rx.cond(
                DashboardState.loading,
                "Atualizando...",
                "Atualizar dados",
            ),

            on_click=DashboardState.refresh_data,

            background=COLOR_HEADER,
            color="white",
            border_radius="7px",
            padding_x="1rem",
            cursor="pointer",

            disabled=DashboardState.loading,

            _hover={
                "background": "#124E8A",
            },
        ),

        width="100%",
        align="center",
        spacing="4",
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
            min_height="104px",
            display="flex",
            align_items="center",
            justify_content="center",
            position="relative",
            botton="2rem",

            border_top_right_radius="60px",
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
            min_height="104px",
            display="flex",
            align_items="center",
            justify_content="center",

            border_top_right_radius="68px",
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


def panorama_section() -> rx.Component:
    """Panorama geral do Programa de Metas."""

    return rx.vstack(
        rx.box(
            rx.center(
                rx.text(
                    "PANORAMA GERAL DO BALANÇO DO PDM 25/28",
                    color="white",
                    font_size={
                        "initial": "1.45rem",
                        "md": "2rem",
                        "lg": "2.6rem",
                    },
                    font_weight=FONT_WEIGHT_BOLD,
                    text_align="center",
                ),

                min_height="128px",
                width="100%",
            ),

            background=COLOR_HEADER,
            width="100%",
            border_top_right_radius="68px",
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
        ),

        width="100%",
        spacing="0",
        align="stretch",
    )


# ============================================================
# ANDAMENTO
# ============================================================

def progress_item(
    title: str,
    value,
    percentage,
    color_scheme: str,
) -> rx.Component:
    """Linha de progresso das metas."""

    return rx.vstack(
        rx.hstack(
            rx.text(
                title,
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_SM,
                font_weight=FONT_WEIGHT_MEDIUM,
            ),

            rx.spacer(),

            rx.hstack(
                rx.text(
                    value,
                    color=TEXT_PRIMARY,
                    font_size=FONT_SIZE_MD,
                    font_weight=FONT_WEIGHT_BOLD,
                ),

                rx.text(
                    "(",
                    percentage,
                    "%)",
                    color=TEXT_SECONDARY,
                    font_size=FONT_SIZE_SM,
                ),

                spacing="1",
                align="center",
            ),

            width="100%",
            align="center",
        ),

        rx.progress(
            value=value,
            max=DashboardState.total_metas,
            width="100%",
            color_scheme=color_scheme,
        ),

        spacing="2",
        width="100%",
        align="stretch",
    )


def andamento_panel() -> rx.Component:
    """Indicadores de andamento."""

    return rx.vstack(
        rx.text(
            "Andamento",
            color=TEXT_PRIMARY,
            font_size=FONT_SIZE_MD,
            font_weight=FONT_WEIGHT_BOLD,
        ),

        progress_item(
            "Atingidas",
            DashboardState.metas_atingidas,
            DashboardState.percentual_atingidas,
            "green",
        ),

        progress_item(
            "Em progresso",
            DashboardState.metas_em_progresso,
            DashboardState.percentual_em_progresso,
            "cyan",
        ),

        progress_item(
            "Em planejamento",
            DashboardState.metas_em_planejamento,
            DashboardState.percentual_em_planejamento,
            "orange",
        ),

        spacing="5",
        width="100%",
        align="stretch",
    )


# ============================================================
# SITUAÇÃO
# ============================================================

def situation_item(item) -> rx.Component:
    """Item da classificação de risco."""

    return rx.hstack(
        rx.text(
            item["nome"],
            color=TEXT_PRIMARY,
            font_size=FONT_SIZE_SM,
        ),

        rx.spacer(),

        rx.box(
            rx.text(
                item["quantidade"],
                color="white",
                font_size=FONT_SIZE_SM,
                font_weight=FONT_WEIGHT_BOLD,
            ),

            background=COLOR_TOTAL,
            border_radius="4px",
            min_width="38px",
            padding="0.3rem 0.55rem",
            text_align="center",
        ),

        width="100%",
        align="center",
        padding_y="0.25rem",
    )


def situation_panel() -> rx.Component:
    """Indicadores de situação."""

    return rx.vstack(
        rx.text(
            "Situação das metas",
            color=TEXT_PRIMARY,
            font_size=FONT_SIZE_MD,
            font_weight=FONT_WEIGHT_BOLD,
        ),

        rx.text(
            "Classificação de cronograma e risco",
            color=TEXT_SECONDARY,
            font_size=FONT_SIZE_SM,
        ),

        rx.vstack(
            rx.foreach(
                DashboardState.situacao_resumo,
                situation_item,
            ),

            spacing="1",
            width="100%",
        ),

        spacing="3",
        width="100%",
        align="stretch",
    )


# ============================================================
# ANÁLISE GERAL
# ============================================================

def analysis_section() -> rx.Component:
    """Bloco principal de análise."""

    return rx.box(
        rx.vstack(
            rx.text(
                "análise geral das metas",
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_XL,
                font_weight=FONT_WEIGHT_BOLD,
            ),

            rx.text(
                "Leitura consolidada do andamento e da situação "
                "das metas do Programa.",
                color=TEXT_SECONDARY,
                font_size=FONT_SIZE_SM,
            ),

            rx.grid(
                andamento_panel(),
                situation_panel(),

                columns={
                    "initial": "1",
                    "lg": "1.4fr 1fr",
                },

                spacing="8",
                width="100%",
            ),

            spacing="5",
            width="100%",
            align="stretch",
        ),

        background=SURFACE,

        border=f"2px solid {PANEL_BORDER}",
        border_top_right_radius="82px",

        padding={
            "initial": "1.25rem",
            "md": "2rem",
        },

        width="100%",
    )


# ============================================================
# PRAZOS
# ============================================================

def prazo_item(item) -> rx.Component:
    """Exibe prazo e quantidade de metas."""

    return rx.hstack(
        rx.box(
            rx.text(
                item["quantidade"],
                color="white",
                font_weight=FONT_WEIGHT_BOLD,
                font_size=FONT_SIZE_SM,
            ),

            background=COLOR_TOTAL,
            border_radius="3px",
            width="42px",
            min_width="42px",
            padding_y="0.4rem",
            text_align="center",
        ),

        rx.text(
            item["nome"],
            color=TEXT_PRIMARY,
            font_size=FONT_SIZE_SM,
        ),

        spacing="3",
        align="center",
        width="100%",
    )


def prazo_section() -> rx.Component:
    """Distribuição das metas por prazo."""

    return rx.box(
        rx.vstack(
            rx.text(
                "prazos das metas",
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_XL,
                font_weight=FONT_WEIGHT_BOLD,
            ),

            rx.text(
                "Distribuição das entregas previstas por semestre.",
                color=TEXT_SECONDARY,
                font_size=FONT_SIZE_SM,
            ),

            rx.grid(
                rx.foreach(
                    DashboardState.prazo_resumo,
                    prazo_item,
                ),

                columns={
                    "initial": "1",
                    "sm": "2",
                    "lg": "3",
                },

                spacing="4",
                width="100%",
            ),

            spacing="5",
            width="100%",
            align="stretch",
        ),

        background=SURFACE,
        border=f"2px solid {PANEL_BORDER}",
        border_top_right_radius="82px",
        padding="2rem",
        width="100%",
        height="100%",
    )


# ============================================================
# ORÇAMENTO
# ============================================================

def budget_row(
    title: str,
    value,
    description,
) -> rx.Component:
    """Linha financeira."""

    return rx.vstack(
        rx.text(
            title,
            color=TEXT_SECONDARY,
            font_size=FONT_SIZE_SM,
        ),

        rx.text(
            value,
            color=TEXT_PRIMARY,
            font_size=FONT_SIZE_XL,
            font_weight=FONT_WEIGHT_BOLD,
        ),

        description,

        spacing="1",
        width="100%",
        align="start",
    )


def budget_section() -> rx.Component:
    """Resumo financeiro."""

    return rx.box(
        rx.vstack(
            rx.text(
                "orçamento das metas",
                color=TEXT_PRIMARY,
                font_size=FONT_SIZE_XL,
                font_weight=FONT_WEIGHT_BOLD,
            ),

            rx.center(
                rx.vstack(
                    rx.text(
                        "PREVISÃO TOTAL",
                        color=TEXT_SECONDARY,
                        font_size=FONT_SIZE_SM,
                        font_weight=FONT_WEIGHT_SEMIBOLD,
                    ),

                    rx.text(
                        DashboardState.orcamento_previsao,
                        color=COLOR_HEADER,
                        font_size="1.7rem",
                        font_weight=FONT_WEIGHT_BOLD,
                        text_align="center",
                    ),

                    spacing="1",
                    align="center",
                ),

                width="100%",
                padding_y="1rem",
            ),

            rx.divider(),

            budget_row(
                "Empenhado",
                DashboardState.orcamento_empenhado,

                rx.text(
                    DashboardState.percentual_empenhado,
                    "% da previsão",
                    color=TEXT_SECONDARY,
                    font_size=FONT_SIZE_SM,
                ),
            ),

            budget_row(
                "Liquidado",
                DashboardState.orcamento_liquidado,

                rx.text(
                    DashboardState.percentual_liquidado,
                    "% da previsão",
                    color=TEXT_SECONDARY,
                    font_size=FONT_SIZE_SM,
                ),
            ),

            rx.text(
                DashboardState.metas_com_previsao,
                " metas possuem previsão orçamentária.",
                color=TEXT_SECONDARY,
                font_size=FONT_SIZE_SM,
            ),

            spacing="5",
            width="100%",
            align="stretch",
        ),

        background=SURFACE,
        border=f"2px solid {PANEL_BORDER}",
        border_top_left_radius="82px",
        padding="2rem",
        width="100%",
        height="100%",
    )


# ============================================================
# MENSAGENS
# ============================================================

def dashboard_messages() -> rx.Component:
    """Mensagens de sincronização e erro."""

    return rx.vstack(
        rx.cond(
            DashboardState.sync_message != "",

            rx.box(
                rx.text(
                    DashboardState.sync_message,
                    font_size=FONT_SIZE_SM,
                    color=COLOR_GREEN,
                ),

                width="100%",
                padding="0.65rem 0.9rem",
                background="rgba(40, 129, 64, 0.08)",
                border_radius="8px",
            ),
        ),

        rx.cond(
            DashboardState.error_message != "",

            rx.box(
                rx.text(
                    DashboardState.error_message,
                    font_size=FONT_SIZE_SM,
                    color=COLOR_RED,
                ),

                width="100%",
                padding="0.65rem 0.9rem",
                background="rgba(236, 32, 36, 0.08)",
                border_radius="8px",
            ),
        ),

        width="100%",
        spacing="2",
    )


# ============================================================
# CONTEÚDO
# ============================================================

def dashboard_content() -> rx.Component:
    """Conteúdo principal do dashboard."""

    return rx.vstack(
        dashboard_header(),

        dashboard_messages(),

        panorama_section(),

        analysis_section(),

        rx.grid(
            prazo_section(),
            budget_section(),

            columns={
                "initial": "1",
                "lg": "2fr 1fr",
            },

            spacing="8",
            width="100%",
            align_items="stretch",
        ),

        width="100%",
        spacing="7",
        align="stretch",

        padding_bottom="2rem",

        on_mount=DashboardState.load_summary,
    )


def dashboard_page() -> rx.Component:
    """Página principal do painel administrativo."""

    return admin_layout(
        dashboard_content()
    )