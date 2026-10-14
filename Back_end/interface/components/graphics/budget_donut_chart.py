from decimal import Decimal

import plotly.graph_objects as go
import reflex as rx

from Back_end.interface.theme.colors import (
    CYAN_LIGHT,
    YELLOW_ORANGE,
    NAVY,
)


# ============================================================
# HELPERS
# ============================================================

def _to_decimal(
    value: Decimal | int | float | None,
) -> Decimal:
    """Converte valores financeiros para Decimal."""

    return Decimal(str(value or 0))


def _format_brl(
    value: Decimal,
) -> str:
    """Formata valor monetário no padrão brasileiro."""

    formatted = (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {formatted}"


def _format_brl_compact(
    value: Decimal,
) -> str:
    """Formata valores grandes para exibição no centro do donut."""

    absolute = abs(value)

    if absolute >= Decimal("1000000000"):
        compact = value / Decimal("1000000000")

        return (
            f"R$ {compact:.2f} bi"
            .replace(".", ",")
        )

    if absolute >= Decimal("1000000"):
        compact = value / Decimal("1000000")

        return (
            f"R$ {compact:.2f} mi"
            .replace(".", ",")
        )

    if absolute >= Decimal("1000"):
        compact = value / Decimal("1000")

        return (
            f"R$ {compact:.2f} mil"
            .replace(".", ",")
        )

    return _format_brl(value)


# ============================================================
# FIGURA
# ============================================================

def build_budget_figure(
    previsao,
    empenhado,
    liquidado,
) -> go.Figure:
    """
    Cria o gráfico de orçamento.

    As fatias são mutuamente exclusivas:
    liquidado, empenhado ainda não liquidado
    e saldo ainda não empenhado.
    """

    previsao_decimal = _to_decimal(
        previsao
    )

    empenhado_decimal = _to_decimal(
        empenhado
    )

    liquidado_decimal = _to_decimal(
        liquidado
    )

    # Parte do empenhado que ainda não foi liquidada.
    empenhado_a_liquidar = max(
        empenhado_decimal - liquidado_decimal,
        Decimal("0"),
    )

    # Parte da previsão que ainda não foi empenhada.
    saldo_nao_empenhado = max(
        previsao_decimal - empenhado_decimal,
        Decimal("0"),
    )

    labels = [
        "Liquidado",
        "Empenhado a liquidar",
        "Saldo da previsão",
    ]

    values = [
        float(liquidado_decimal),
        float(empenhado_a_liquidar),
        float(saldo_nao_empenhado),
    ]

    formatted_values = [
        _format_brl(liquidado_decimal),
        _format_brl(empenhado_a_liquidar),
        _format_brl(saldo_nao_empenhado),
    ]

    figure = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,

                hole=0.58,

                sort=False,

                direction="clockwise",

                marker={
                    "colors": [
                        CYAN_LIGHT,
                        YELLOW_ORANGE,
                        NAVY,
                    ],

                    "line": {
                        "color": "rgba(255,255,255,0.25)",
                        "width": 1,
                    },
                },

                textinfo="percent",

                textposition="inside",

                textfont={
                    "size": 13,
                    "color": "#FFFFFF",
                },

                customdata=formatted_values,

                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "%{customdata}<br>"
                    "%{percent}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    # ========================================================
    # LAYOUT
    # ========================================================

    figure.update_layout(
        title={
            "text": (
                "<b>ORÇAMENTO DAS METAS</b>"
                "<br>"
                "<span style='font-size:13px'>"
                "Execução financeira em relação "
                "à previsão total"
                "</span>"
            ),

            "x": 0.02,
            "xanchor": "left",

            "y": 0.96,
            "yanchor": "top",
        },

        height=400,

        autosize=True,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin={
            "l": 20,
            "r": 20,
            "t": 90,
            "b": 25,
        },

        legend={
            "orientation": "v",

            "x": 0.73,
            "y": 0.62,

            "xanchor": "left",
            "yanchor": "middle",

            "font": {
                "size": 13,
            },

            "bgcolor": "rgba(0,0,0,0)",
        },

        # Valor total no centro do donut.
        annotations=[
            {
                "text": (
                    "<span style='font-size:11px'>"
                    "PREVISÃO TOTAL"
                    "</span>"
                    "<br>"
                    "<b>"
                    f"{_format_brl_compact(previsao_decimal)}"
                    "</b>"
                ),

                "x": 0.36,
                "y": 0.50,

                "showarrow": False,

                "align": "center",

                "font": {
                    "size": 16,
                },
            }
        ],
    )

    # Deixa espaço à direita para a legenda.
    figure.update_traces(
        domain={
            "x": [0.03, 0.68],
            "y": [0.05, 0.95],
        }
    )

    return figure


# ============================================================
# COMPONENTE REFLEX
# ============================================================

def budget_donut_chart(
    figure,
) -> rx.Component:
    """Renderiza o gráfico de orçamento no dashboard."""

    return rx.box(
        rx.plotly(
            data=figure,

            config={
                "displayModeBar": False,
                "responsive": True,
                "scrollZoom": False,
            },

            use_resize_handler=True,
            width="100%",
            height="100%",
        ),
        width="100%",
        height="430px",
        min_height="430px",
        min_width="0",
        overflow="visible",
    )