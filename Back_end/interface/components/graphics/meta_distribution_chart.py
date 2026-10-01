import plotly.graph_objects as go
from plotly.subplots import make_subplots

import reflex as rx

from Back_end.interface.theme.colors import ( GREEN_DARK, YELLOW_ORANGE, ORANGE_RED, RED, CYAN_LIGHT, CYAN_MEDIUM, CYAN_DARK, BLUE_DARK, BLUE, NAVY, PURPLE_DARK, PURPLE_MEDIUM, PURPLE_RED,)


# ============================================================
# CORES
# ============================================================

SITUACAO_COLORS = {
    "Dentro do cronograma": GREEN_DARK,
    "Risco baixo/médio": YELLOW_ORANGE,
    "Risco alto/muito alto": ORANGE_RED,
    "Meta atingida": CYAN_LIGHT,
    "Meta comprometida": RED,
}


PRAZO_COLORS = {
    "1º sem/2025": CYAN_LIGHT,
    "2º sem/2025": CYAN_MEDIUM,
    "1º sem/2026": CYAN_DARK,
    "2º sem/2026": BLUE_DARK,
    "1º sem/2027": BLUE,
    "2º sem/2027": NAVY,
    "1º sem/2028": PURPLE_DARK,
    "2º sem/2028": PURPLE_MEDIUM,
    "Sem previsão": PURPLE_RED,
}


# ============================================================
# ORDENAÇÃO
# ============================================================

SITUACAO_ORDER = [
    "Dentro do cronograma",
    "Risco baixo/médio",
    "Risco alto/muito alto",
    "Meta atingida",
    "Meta comprometida",
]


PRAZO_ORDER = [
    "1º sem/2025",
    "2º sem/2025",
    "1º sem/2026",
    "2º sem/2026",
    "1º sem/2027",
    "2º sem/2027",
    "1º sem/2028",
    "2º sem/2028",
    "Sem previsão",
]


# ============================================================
# LABELS CURTOS
# ============================================================

SITUACAO_LABELS = {
    "Dentro do cronograma": "Dentro do<br>cronograma",
    "Risco baixo/médio": "Risco<br>baixo/médio",
    "Risco alto/muito alto": "Risco<br>alto/muito alto",
    "Meta atingida": "Meta<br>atingida",
    "Meta comprometida": "Meta<br>comprometida",
}


PRAZO_LABELS = {
    "1º sem/2025": "1º sem<br>2025",
    "2º sem/2025": "2º sem<br>2025",
    "1º sem/2026": "1º sem<br>2026",
    "2º sem/2026": "2º sem<br>2026",
    "1º sem/2027": "1º sem<br>2027",
    "2º sem/2027": "2º sem<br>2027",
    "1º sem/2028": "1º sem<br>2028",
    "2º sem/2028": "2º sem<br>2028",
    "Sem previsão": "Sem<br>previsão",
}


# ============================================================
# HELPERS
# ============================================================

def _normalize_items( items: list[dict], order: list[str],) -> list[dict]:
    """Organiza os dados de acordo com a ordem do dashboard."""

    values = {
        str(item.get("nome", "")): int(
            item.get("quantidade", 0)
        )
        for item in items
    }

    return [
        {
            "nome": nome,
            "quantidade": values.get(nome, 0),
        }
        for nome in order
    ]


# ============================================================
# CONSTRUÇÃO DO GRÁFICO
# ============================================================

def build_meta_distribution_figure( situacao: list[dict], prazos: list[dict],) -> go.Figure:
    """
    Cria uma única figura Plotly contendo
    situação das metas e distribuição por prazo.
    """

    situacao_data = _normalize_items(
        situacao,
        SITUACAO_ORDER,
    )

    prazo_data = _normalize_items(
        prazos,
        PRAZO_ORDER,
    )

    total_situacao = sum(
        item["quantidade"]
        for item in situacao_data
    )

    total_prazo = sum(
        item["quantidade"]
        for item in prazo_data
    )

    # ========================================================
    # UMA ÚNICA FIGURA, DOIS PAINÉIS
    # ========================================================

    figure = make_subplots(
        rows=1,
        cols=2,

        column_widths=[
            0.40,
            0.60,
        ],

        horizontal_spacing=0.08,

        subplot_titles=[
            "SITUAÇÃO DAS METAS",
            "PRAZOS DAS METAS",
        ],
    )

    # ========================================================
    # SITUAÇÃO
    # ========================================================

    for item in situacao_data:
        nome = item["nome"]
        quantidade = item["quantidade"]

        percentual = (
            quantidade / total_situacao * 100
            if total_situacao > 0
            else 0
        )

        figure.add_trace(
            go.Bar(
                x=[
                    SITUACAO_LABELS.get(
                        nome,
                        nome,
                    )
                ],

                y=[
                    quantidade
                ],

                name=nome,

                marker_color=SITUACAO_COLORS.get(
                    nome,
                    "#8B92A0",
                ),

                text=[
                    quantidade
                ],

                textposition="outside",

                textfont={
                    "size": 13,
                },

                customdata=[
                    [percentual]
                ],

                hovertemplate=(
                    f"<b>{nome}</b><br>"
                    "%{y} metas<br>"
                    "%{customdata[0]:.1f}% do total"
                    "<extra></extra>"
                ),

                showlegend=False,
            ),

            row=1,
            col=1,
        )

    # ========================================================
    # PRAZOS
    # ========================================================

    for item in prazo_data:
        nome = item["nome"]
        quantidade = item["quantidade"]

        percentual = (
            quantidade / total_prazo * 100
            if total_prazo > 0
            else 0
        )

        figure.add_trace(
            go.Bar(
                x=[
                    PRAZO_LABELS.get(
                        nome,
                        nome,
                    )
                ],

                y=[
                    quantidade
                ],

                name=nome,

                marker_color=PRAZO_COLORS.get(
                    nome,
                    "#8B92A0",
                ),

                text=[
                    quantidade
                ],

                textposition="outside",

                textfont={
                    "size": 13,
                },

                customdata=[
                    [percentual]
                ],

                hovertemplate=(
                    f"<b>{nome}</b><br>"
                    "%{y} metas<br>"
                    "%{customdata[0]:.1f}% do total"
                    "<extra></extra>"
                ),

                showlegend=False,
            ),

            row=1,
            col=2,
        )

    # ========================================================
    # MAIOR VALOR
    # ========================================================

    maior_valor = max(
        [
            item["quantidade"]
            for item in situacao_data + prazo_data
        ]
        or [1]
    )

    limite_y = maior_valor * 1.18

    # ========================================================
    # EIXOS
    # ========================================================

    figure.update_xaxes(
        showgrid=False,
        showline=False,
        zeroline=False,
        fixedrange=True,

        tickfont={
            "size": 11,
        },
    )

    figure.update_yaxes(
        range=[
            0,
            limite_y,
        ],

        showgrid=True,

        gridcolor="rgba(140, 150, 170, 0.18)",

        showline=False,
        zeroline=False,

        fixedrange=True,

        tickfont={
            "size": 11,
        },
    )

    # Tiramos os números do segundo eixo Y.
    figure.update_yaxes(
        showticklabels=False,
        row=1,
        col=2,
    )

    # ========================================================
    # LAYOUT GERAL
    # ========================================================

    figure.update_layout(
        title={
            "text": (
                "<b>DISTRIBUIÇÃO DAS METAS</b>"
                "<br>"
                "<span style='font-size:13px'>"
                "Classificação de cronograma, risco "
                "e prazos previstos"
                "</span>"
            ),

            "x": 0.02,
            "xanchor": "left",

            "y": 0.96,
            "yanchor": "top",
        },

        barmode="group",

        bargap=0.22,

        bargroupgap=0.08,

        height=430,

        autosize=True,

        paper_bgcolor="rgba(0, 0, 0, 0)",

        plot_bgcolor="rgba(0, 0, 0, 0)",

        margin={
            "l": 55,
            "r": 20,
            "t": 95,
            "b": 70,
        },

        hovermode="closest",

        showlegend=False,

        font={
            "family": "Arial, sans-serif",
        },
    )

    # ========================================================
    # TÍTULOS DOS SUBPLOTS
    # ========================================================

    for annotation in figure.layout.annotations:
        annotation.font = {
            "size": 14,
        }

    return figure


# ============================================================
# COMPONENTE REFLEX
# ============================================================

def meta_distribution_chart( figure, situacao=None, prazos=None,) -> rx.Component:
    """
    Renderiza o gráfico Plotly.

    situacao e prazos continuam aceitos para evitar
    necessidade de alterar a chamada atual no dashboard.
    A figura já contém todas as informações visuais.
    """

    return rx.box(
        rx.plotly(
            data=figure,

            config={
                "displayModeBar": False,
                "responsive": True,
                "scrollZoom": False,
            },

            use_resize_handler=True,
        ),

        width="100%",
        height="430px",
        min_height="430px",

        overflow="hidden",
    )