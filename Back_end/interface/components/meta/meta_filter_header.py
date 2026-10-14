import reflex as rx

from Back_end.interface.state.meta.meta_list_state import (MetaListState,)
from Back_end.interface.theme.typography import (FONT_FAMILY_PRIMARY,FONT_FAMILY_SECUNDARY,FONT_WEIGHT_MEDIUM,)

# ============================================================
# CORES
# ============================================================

FILTER_BACKGROUND = rx.color_mode_cond("#EAF3F8","#2C4784",)
FILTER_CONTROL_BACKGROUND = rx.color_mode_cond("#FFFFFF","#20335F",)
FILTER_CONTROL_HOVER = rx.color_mode_cond("#F4F8FB","#2472A7",)
FILTER_TITLE = rx.color_mode_cond("#272361","#4CC7E2",)
FILTER_TEXT = rx.color_mode_cond("#272361","#FFFFFF",)
FILTER_TEXT_MUTED = rx.color_mode_cond("#61697A","rgba(255, 255, 255, 0.88)",)
FILTER_BORDER = rx.color_mode_cond("#D4E1E8", "rgba(255, 255, 255, 0.10)",)


# ============================================================
# SELECT
# ============================================================

def filter_select( label: str, options, value, on_change, disabled=False, ) -> rx.Component:
    """Select visual utilizado nos filtros das metas."""

    return rx.select.root(
        rx.select.trigger(
            placeholder=label,
            width="120px",
            height="46px",
            background=FILTER_CONTROL_BACKGROUND,
            color=FILTER_TEXT,
            border=f"1px solid {FILTER_BORDER}",
            border_radius="12px",
            padding_x="0.85rem",
            font_family=FONT_FAMILY_SECUNDARY,
            font_size="1.05rem",
            cursor="pointer",
            _hover={"background": FILTER_CONTROL_HOVER,},
        ),

        rx.select.content(
            rx.select.group(
                rx.foreach(
                    options,
                    lambda option: rx.select.item( option, value=option, ),
                ),
            ),
            position="popper",
            max_height="280px",
        ),
        value=value,
        on_change=on_change,
        disabled=disabled,
    )


# ============================================================
# PESQUISA
# ============================================================

def search_input() -> rx.Component:
    """Pesquisa metas por código ou título."""

    return rx.input(
        rx.input.slot(
            rx.icon(
                tag="search",
                size=21,
                color=FILTER_TEXT,
            ),
        ),
        placeholder="Pesquisar meta...",
        value=MetaListState.search_text,
        on_change=MetaListState.update_search_text,
        width="100%",
        min_width="210px",
        max_width="280px",
        height="46px",
        background=FILTER_CONTROL_BACKGROUND,
        color=FILTER_TEXT,
        border=f"1px solid {FILTER_BORDER}",
        border_radius="12px",
        font_family=FONT_FAMILY_PRIMARY,
        font_size="0.88rem",
        _placeholder={"color": FILTER_TEXT_MUTED,},
    )


# ============================================================
# LIMPAR FILTROS
# ============================================================

def clear_filters_button() -> rx.Component:
    """Limpa pesquisa e filtros selecionados."""

    return rx.button(
        "LIMPAR FILTROS",

        on_click=MetaListState.clear_filters,
        height="34px",
        padding_x="0.9rem",
        background="#65C8DE",
        color="#173D67",
        border_radius="18px",
        font_family=FONT_FAMILY_SECUNDARY,
        font_size="0.8rem",
        cursor="pointer",
        _hover={"background": "#86D7E8",},
    )


# ============================================================
# APRESENTAÇÃO
# ============================================================

def meta_filter_intro() -> rx.Component:
    """Título e descrição da área de metas."""

    return rx.vstack(
        rx.text(
            "METAS",
            color=FILTER_TITLE,
            font_family=FONT_FAMILY_SECUNDARY,
            font_size={"initial": "2.1rem", "md": "2.5rem",},
            line_height="1",
            white_space="nowrap",
        ),

        rx.text(
            "Pesquise e selecione uma meta "
            "para visualizar sua ficha.",
            color=FILTER_TEXT_MUTED,
            font_family=FONT_FAMILY_PRIMARY,
            font_size="0.82rem",
            line_height="1.25",
            width="190px",
        ),
        spacing="2",
        align="start",
        min_width="205px",
    )


# ============================================================
# FILTROS
# ============================================================

def meta_filter_controls() -> rx.Component:
    """Controles de filtro e busca."""

    return rx.hstack(
        filter_select(
            label="EIXO",
            options=MetaListState.eixos_disponiveis,
            value=MetaListState.eixo_filter,
            on_change=MetaListState.update_eixo_filter,
        ),

        filter_select(
            label="ÓRGÃO",
            options=MetaListState.orgaos_disponiveis,
            value=MetaListState.orgao_filter,
            on_change=MetaListState.update_orgao_filter,
        ),

        filter_select(
            label="TEMA",
            options=MetaListState.temas_disponiveis,
            value=MetaListState.tema_filter,
            on_change=MetaListState.update_tema_filter,
        ),
        # Região já fica preparada para o futuro.
        # Enquanto não houver dados, aparece desabilitada.
        filter_select(
            label="REGIÃO",
            options=MetaListState.regioes_disponiveis,
            value=MetaListState.regiao_filter,
            on_change=MetaListState.update_regiao_filter,
            disabled=(MetaListState.regioes_disponiveis.length()== 0),
        ),
        clear_filters_button(),
        search_input(),
        spacing="3",
        align="center",
        justify="end",
        flex="1",
        flex_wrap="wrap",
    )


# ============================================================
# COMPONENTE PRINCIPAL
# ============================================================

def meta_filter_header() -> rx.Component:
    """
    Cabeçalho da listagem de metas com título,
    filtros e pesquisa.
    """

    return rx.box(
        rx.hstack(
            meta_filter_intro(),
            meta_filter_controls(),
            width="100%",
            align="center",
            justify="between",
            spacing="6",
            flex_wrap="wrap",
        ),

        width="100%",
        padding={ "initial": "1.25rem", "md": "1.5rem 2rem", },
    )