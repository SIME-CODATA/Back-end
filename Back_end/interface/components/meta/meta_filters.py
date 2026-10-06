import reflex as rx

from Back_end.interface.state.meta.meta_list_state import (
    MetaListState,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
    FONT_WEIGHT_MEDIUM,
    FONT_WEIGHT_SEMIBOLD,
)


# ============================================================
# CORES
# ============================================================

FILTER_BACKGROUND = rx.color_mode_cond(
    "#EAF3F8",
    "#293F7B",
)

FILTER_CONTROL_BACKGROUND = rx.color_mode_cond(
    "#FFFFFF",
    "#17639A",
)

FILTER_CONTROL_HOVER = rx.color_mode_cond(
    "#E6F3F8",
    "#1C70A8",
)

FILTER_TITLE = rx.color_mode_cond(
    "#272361",
    "#4BC4E2",
)

FILTER_TEXT = rx.color_mode_cond(
    "#272361",
    "#FFFFFF",
)

FILTER_TEXT_MUTED = rx.color_mode_cond(
    "#61697A",
    "rgba(255, 255, 255, 0.82)",
)

FILTER_BORDER = rx.color_mode_cond(
    "#C9DCE6",
    "rgba(255, 255, 255, 0.08)",
)


# ============================================================
# SELECT
# ============================================================

def filter_select(
    label: str,
    options,
    value,
    on_change,
) -> rx.Component:
    """Select reutilizável da barra de filtros."""

    return rx.select.root(
        rx.select.trigger(
            placeholder=label,

            width="112px",
            height="46px",

            background=FILTER_CONTROL_BACKGROUND,
            color=FILTER_TEXT,

            border=f"1px solid {FILTER_BORDER}",
            border_radius="12px",

            padding_x="0.85rem",

            font_family=FONT_FAMILY_SECUNDARY,
            font_size="1.05rem",

            cursor="pointer",

            _hover={
                "background": FILTER_CONTROL_HOVER,
            },
        ),

        rx.select.content(
            rx.select.group(
                rx.foreach(
                    options,
                    lambda option: rx.select.item(
                        option,
                        value=option,
                    ),
                ),
            ),

            position="popper",
        ),

        value=value,
        on_change=on_change,
    )


# ============================================================
# BUSCA
# ============================================================

def search_field() -> rx.Component:
    """Campo de busca por número ou título da meta."""

    return rx.input(
        rx.input.slot(
            rx.icon(
                tag="search",
                size=21,
            ),
        ),

        placeholder="Pesquisar meta...",

        value=MetaListState.search_text,
        on_change=MetaListState.update_search_text,

        width={
            "initial": "100%",
            "lg": "220px",
        },

        height="46px",

        background=FILTER_CONTROL_BACKGROUND,
        color=FILTER_TEXT,

        border=f"1px solid {FILTER_BORDER}",
        border_radius="12px",

        font_family=FONT_FAMILY_PRIMARY,

        _placeholder={
            "color": FILTER_TEXT_MUTED,
        },
    )


# ============================================================
# LIMPAR FILTROS
# ============================================================

def clear_filter_button() -> rx.Component:
    """Limpa busca e filtros selecionados."""

    return rx.button(
        rx.text(
            "LIMPAR",
            rx.el.br(),
            "FILTRO",

            font_family=FONT_FAMILY_SECUNDARY,
            font_size="0.78rem",
            line_height="0.85",
            text_align="center",
        ),

        on_click=MetaListState.clear_filters,

        width="62px",
        height="34px",

        padding="0",

        background="#65C8DE",
        color="#173D67",

        border_radius="18px",

        cursor="pointer",

        _hover={
            "background": "#82D7E8",
        },
    )


# ============================================================
# COMPONENTE PRINCIPAL
# ============================================================

def meta_filters() -> rx.Component:
    """Cabeçalho da página de metas com filtros e pesquisa."""

    return rx.box(
        rx.hstack(
            # ------------------------------------------------
            # Apresentação
            # ------------------------------------------------

            rx.vstack(
                rx.text(
                    "METAS",

                    color=FILTER_TITLE,

                    font_family=FONT_FAMILY_SECUNDARY,
                    font_size="2.35rem",
                    line_height="1",

                    white_space="nowrap",
                ),

                rx.text(
                    "Pesquise e selecione uma meta "
                    "para visualizar sua ficha.",

                    color=FILTER_TEXT_MUTED,

                    font_family=FONT_FAMILY_PRIMARY,
                    font_size="0.82rem",

                    max_width="190px",
                    line_height="1.25",
                ),

                spacing="2",
                align="start",

                min_width="205px",
            ),

            # ------------------------------------------------
            # Controles
            # ------------------------------------------------

            rx.hstack(
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

                filter_select(
                    label="REGIÃO",
                    options=MetaListState.regioes_disponiveis,
                    value=MetaListState.regiao_filter,
                    on_change=MetaListState.update_regiao_filter,
                ),

                clear_filter_button(),

                search_field(),

                spacing="3",
                align="center",

                flex="1",
                justify="end",

                flex_wrap="wrap",
            ),

            width="100%",
            align="center",
            spacing="6",

            flex_wrap="wrap",
        ),

        width="100%",

        padding={
            "initial": "1.25rem",
            "md": "1.5rem 2rem",
        },

        background=FILTER_BACKGROUND,

        border_bottom=f"1px solid {FILTER_BORDER}",

        border_radius="14px",
    )