import reflex as rx

from Back_end.interface.state.meta.meta_list_state import (MetaListState,)
from Back_end.interface.theme.typography import (FONT_FAMILY_PRIMARY,FONT_FAMILY_SECUNDARY,)

# ============================================================
# CORES
# ============================================================

DOCK_BACKGROUND = rx.color_mode_cond("#FFFFFF","#20335F",)
DOCK_PANEL_BACKGROUND = rx.color_mode_cond("#F8FBFD","#18294D",)
DOCK_CONTROL_BACKGROUND = rx.color_mode_cond("#FFFFFF","#20335F",)
DOCK_CONTROL_HOVER = rx.color_mode_cond("#F0F5F8","#2C4784",)
DOCK_BORDER = rx.color_mode_cond("#D4E1E8","rgba(255, 255, 255, 0.12)",)
DOCK_TEXT = rx.color_mode_cond("#272361","#FFFFFF",)
DOCK_MUTED = rx.color_mode_cond("#667085","rgba(255, 255, 255, 0.75)",)
DOCK_ACCENT = "#65C8DE"
DOCK_ACCENT_TEXT = "#173D67"

# ============================================================
# SELECT
# ============================================================

def filter_select( label: str, options, value, on_change, disabled=False,) -> rx.Component:
    """
    Select reutilizado pelo painel retrátil
    de filtros.
    """

    return rx.vstack(
        rx.text( label, color=DOCK_MUTED, font_family=FONT_FAMILY_PRIMARY, font_size="0.66rem", font_weight="700", line_height="1",),

        rx.select.root(
            rx.select.trigger(placeholder="Todos",width="100%",height="42px",background=DOCK_CONTROL_BACKGROUND,color=DOCK_TEXT,border=f"1px solid {DOCK_BORDER}",border_radius="10px",padding_x="0.75rem",font_family=FONT_FAMILY_PRIMARY,font_size="0.78rem",cursor="pointer",_hover={"background": DOCK_CONTROL_HOVER,},),

            rx.select.content(
                rx.select.group(
                    rx.foreach(options,lambda option: rx.select.item(option,value=option,),),
                ),
                position="popper", max_height="280px",
            ),
            value=value, on_change=on_change, disabled=disabled,
        ),
        spacing="2",align="start",width="100%",min_width="0",
    )


# ============================================================
# PESQUISA
# ============================================================

def search_input(*, inside_panel: bool = False,) -> rx.Component:
    """Pesquisa metas por número ou título."""

    return rx.input(
        rx.input.slot(
            rx.icon(tag="search",size=17,color=DOCK_TEXT,),
        ),
        placeholder="Pesquisar meta...",
        value=MetaListState.search_text,
        on_change=(MetaListState.update_search_text),
        width=(
            "100%"
            if inside_panel
            else "240px"
        ),
        height="40px",
        background=DOCK_CONTROL_BACKGROUND,
        color=DOCK_TEXT,
        border=f"1px solid {DOCK_BORDER}",
        border_radius="10px",
        font_family=FONT_FAMILY_PRIMARY,
        font_size="0.8rem",
        disabled=MetaListState.loading,
        _placeholder={"color": DOCK_MUTED,},
    )


# ============================================================
# CONTADOR
# ============================================================

def active_filter_badge() -> rx.Component:
    """Contador exibido no botão de filtros."""

    return rx.cond(
        MetaListState.active_filter_count > 0,

        rx.center(
            rx.text(MetaListState.active_filter_count,color="#173D67",font_family=FONT_FAMILY_PRIMARY,font_size="0.64rem",font_weight="700",),
            min_width="20px",
            height="20px",
            padding_x="0.3rem",
            background=DOCK_ACCENT,
            border_radius="999px",
        ),

        rx.box(),
    )


# ============================================================
# BOTÃO FILTROS
# ============================================================

def filter_toggle_button() -> rx.Component:
    """Abre ou fecha o painel de filtros."""

    return rx.button(
        rx.icon(tag="sliders-horizontal",size=17,),
        rx.text("FILTROS",font_family=FONT_FAMILY_SECUNDARY,font_size="0.85rem",),
        active_filter_badge(),
        on_click=(MetaListState.toggle_filter_panel),
        height="40px",
        padding_x="0.8rem",
        background=rx.cond(MetaListState.filter_panel_open,DOCK_CONTROL_HOVER,DOCK_CONTROL_BACKGROUND,),
        color=DOCK_TEXT,
        border=f"1px solid {DOCK_BORDER}",
        border_radius="10px",
        cursor="pointer",
        _hover={"background": DOCK_CONTROL_HOVER,},
        aria_label="Abrir filtros",
    )


# ============================================================
# VOLTAR AO TOPO
# ============================================================

def scroll_top_button() -> rx.Component:
    """Retorna suavemente ao topo da página."""

    return rx.button(
        rx.icon(tag="arrow-up",size=18,),
        on_click=(MetaListState.scroll_to_top),
        width="40px",
        height="40px",
        padding="0",
        background=DOCK_CONTROL_BACKGROUND,
        color=DOCK_TEXT,
        border=f"1px solid {DOCK_BORDER}",
        border_radius="10px",
        cursor="pointer",
        _hover={"background": DOCK_CONTROL_HOVER,},
        aria_label="Voltar ao topo",
    )


# ============================================================
# MAIS FILTROS
# ============================================================

def more_filters_button() -> rx.Component:
    """Mostra ou esconde os filtros secundários."""

    return rx.button(
        rx.icon(
            tag=rx.cond(
                MetaListState.more_filters_open,
                "chevron-up",
                "chevron-down",
            ),
            size=15,
        ),

        rx.text(
            rx.cond(
                MetaListState.more_filters_open,
                "MENOS FILTROS",
                "MAIS FILTROS",
            ),

            font_family=FONT_FAMILY_SECUNDARY,

            font_size="0.75rem",
        ),

        on_click=(
            MetaListState.toggle_more_filters
        ),

        variant="ghost",

        color=DOCK_TEXT,

        cursor="pointer",
    )


# ============================================================
# LIMPAR
# ============================================================

def clear_filters_button() -> rx.Component:
    """Limpa pesquisa e todos os filtros."""

    return rx.button(
        rx.icon(
            tag="rotate-ccw",
            size=14,
        ),

        "LIMPAR",

        on_click=MetaListState.clear_filters,

        height="34px",

        padding_x="0.8rem",

        background=DOCK_ACCENT,

        color=DOCK_ACCENT_TEXT,

        border_radius="999px",

        font_family=FONT_FAMILY_SECUNDARY,

        font_size="0.72rem",

        cursor="pointer",

        _hover={
            "background": "#86D7E8",
        },
    )


# ============================================================
# PAINEL DE FILTROS
# ============================================================

def filter_panel() -> rx.Component:
    """
    Painel retrátil.

    Ele aparece à esquerda do dock,
    mantendo o ponto de controle fixo
    na lateral direita.
    """

    return rx.cond(
        MetaListState.filter_panel_open,

        rx.box(
            rx.vstack(

                # =================================================
                # CABEÇALHO
                # =================================================

                rx.hstack(
                    rx.vstack(
                        rx.text(
                            "FILTRAR METAS",

                            color=DOCK_TEXT,

                            font_family=(
                                FONT_FAMILY_SECUNDARY
                            ),

                            font_size="1.15rem",

                            line_height="1",
                        ),

                        rx.text(
                            "Combine os filtros abaixo "
                            "para refinar a listagem.",

                            color=DOCK_MUTED,

                            font_family=(
                                FONT_FAMILY_PRIMARY
                            ),

                            font_size="0.73rem",
                        ),

                        spacing="1",
                        align="start",
                    ),

                    rx.spacer(),

                    rx.button(
                        rx.icon(
                            tag="x",
                            size=17,
                        ),

                        on_click=(
                            MetaListState
                            .toggle_filter_panel
                        ),

                        variant="ghost",

                        color=DOCK_TEXT,

                        cursor="pointer",

                        aria_label="Fechar filtros",
                    ),

                    width="100%",
                    align="start",
                ),

                # =================================================
                # PESQUISA RESPONSIVA
                # =================================================

                rx.box(
                    search_input(
                        inside_panel=True
                    ),

                    display={
                        "initial": "block",
                        "md": "none",
                    },

                    width="100%",
                ),

                # =================================================
                # FILTROS PRINCIPAIS
                # =================================================

                rx.grid(
                    filter_select(
                        label="EIXO",
                        options=(
                            MetaListState
                            .eixos_disponiveis
                        ),
                        value=(
                            MetaListState
                            .eixo_filter
                        ),
                        on_change=(
                            MetaListState
                            .update_eixo_filter
                        ),
                    ),

                    filter_select(
                        label="ÓRGÃO",
                        options=(
                            MetaListState
                            .orgaos_disponiveis
                        ),
                        value=(
                            MetaListState
                            .orgao_filter
                        ),
                        on_change=(
                            MetaListState
                            .update_orgao_filter
                        ),
                    ),

                    filter_select(
                        label="TEMA",
                        options=(
                            MetaListState
                            .temas_disponiveis
                        ),
                        value=(
                            MetaListState
                            .tema_filter
                        ),
                        on_change=(
                            MetaListState
                            .update_tema_filter
                        ),
                    ),

                    filter_select(
                        label="STATUS",
                        options=(
                            MetaListState
                            .status_disponiveis
                        ),
                        value=(
                            MetaListState
                            .status_filter
                        ),
                        on_change=(
                            MetaListState
                            .update_status_filter
                        ),
                    ),

                    filter_select(
                        label="PROJEÇÃO",
                        options=(
                            MetaListState
                            .projecoes_disponiveis
                        ),
                        value=(
                            MetaListState
                            .projecao_filter
                        ),
                        on_change=(
                            MetaListState
                            .update_projecao_filter
                        ),
                    ),

                    columns={
                        "initial": "1",
                        "sm": "2",
                        "lg": "3",
                    },

                    spacing="3",

                    width="100%",
                ),

                # =================================================
                # MAIS FILTROS
                # =================================================

                rx.box(
                    more_filters_button(),

                    width="100%",
                ),

                rx.cond(
                    MetaListState.more_filters_open,

                    rx.box(
                        filter_select(
                            label="REGIÃO / ZONA",
                            options=(
                                MetaListState
                                .regioes_disponiveis
                            ),
                            value=(
                                MetaListState
                                .regiao_filter
                            ),
                            on_change=(
                                MetaListState
                                .update_regiao_filter
                            ),
                            disabled=(
                                MetaListState
                                .regioes_disponiveis
                                .length()
                                == 0
                            ),
                        ),

                        width={
                            "initial": "100%",
                            "sm": "220px",
                        },

                        padding="0.75rem",

                        background=rx.color_mode_cond(
                            "#EFF5F8",
                            "#20335F",
                        ),

                        border_radius="10px",
                    ),
                ),

                # =================================================
                # RODAPÉ
                # =================================================

                rx.hstack(
                    rx.text(
                        MetaListState
                        .metas_filtradas
                        .length(),

                        " meta(s) encontrada(s)",

                        color=DOCK_MUTED,

                        font_family=(
                            FONT_FAMILY_PRIMARY
                        ),

                        font_size="0.72rem",
                    ),

                    rx.spacer(),

                    clear_filters_button(),

                    width="100%",

                    align="center",
                ),

                spacing="4",

                align="stretch",

                width="100%",
            ),

            # ====================================================
            # POSIÇÃO DO PAINEL
            # ====================================================

            position="absolute",

            right="calc(100% + -21.25rem)",

            top="50%",

            transform="translateY(-110%)",

            width={
                "initial": "calc(100vw - 6rem)",
                "md": "640px",
                "xl": "760px",
            },

            max_height="calc(100dvh - 2rem)",

            overflow_y="auto",

            padding="1rem",

            background=DOCK_PANEL_BACKGROUND,

            border=f"1px solid {DOCK_BORDER}",

            border_radius="16px",

            box_shadow=rx.color_mode_cond(
                "0 14px 40px rgba(21, 37, 63, 0.18)",
                "0 14px 42px rgba(0, 0, 0, 0.32)",
            ),

            z_index="1001",
        ),
    )


# ============================================================
# DOCK
# ============================================================

def meta_filter_dock() -> rx.Component:
    """
    Dock fixo da listagem de metas.

    Pesquisa + filtros + voltar ao topo.
    """

    return rx.box(

        # ----------------------------------------------------
        # Painel abre para a esquerda
        # ----------------------------------------------------

        filter_panel(),

        # ----------------------------------------------------
        # Barra principal
        # ----------------------------------------------------

        rx.hstack(
            rx.box(
                search_input(),

                display={
                    "initial": "none",
                    "md": "block",
                },
            ),

            filter_toggle_button(),

            scroll_top_button(),

            spacing="2",

            align="center",
        ),

        # ====================================================
        # POSIÇÃO
        # ====================================================

        position="fixed",

        right={
            "initial": "0.75rem",
            "md": "4rem",
        },

        top="90%",

        transform="translateY(4%)",

        # ====================================================
        # VISUAL
        # ====================================================

        padding="0.45rem",

        background=DOCK_BACKGROUND,

        border=f"1px solid {DOCK_BORDER}",

        border_radius="13px",

        box_shadow=rx.color_mode_cond(
            "0 7px 22px rgba(24, 40, 68, 0.14)",
            "0 7px 24px rgba(0, 0, 0, 0.28)",
        ),

        z_index="1000",
    )