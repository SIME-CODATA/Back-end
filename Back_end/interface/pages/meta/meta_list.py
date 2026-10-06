import reflex as rx

from Back_end.interface.layouts.admin_layout import (admin_layout,)
from Back_end.interface.state.meta.meta_list_state import (MetaListState,)
from Back_end.access_api.metas.services.meta_list_service import (
    MetaListItem,
)
from Back_end.interface.components.meta.meta_filter_header import (meta_filter_header,)
from Back_end.interface.theme.semantic import ( BORDER, BORDER_DARK, SURFACE, SURFACE_DARK, SURFACE_SECONDARY, SURFACE_SECONDARY_DARK, TEXT_PRIMARY, TEXT_PRIMARY_DARK, TEXT_SECONDARY, TEXT_SECONDARY_DARK,)

from Back_end.interface.theme.typography import (FONT_FAMILY_PRIMARY,FONT_WEIGHT_SEMIBOLD,)


# ============================================================
# CORES REATIVAS
# ============================================================

CARD_BACKGROUND = rx.color_mode_cond(SURFACE,SURFACE_DARK,)
CARD_BACKGROUND_HOVER = rx.color_mode_cond(SURFACE_SECONDARY,SURFACE_SECONDARY_DARK,)
CARD_BORDER = rx.color_mode_cond(BORDER,BORDER_DARK,)
CARD_BORDER_HOVER = rx.color_mode_cond("#272361","#03A8C5",)
CARD_TEXT = rx.color_mode_cond(TEXT_PRIMARY,TEXT_PRIMARY_DARK,)
CARD_TEXT_SECONDARY = rx.color_mode_cond(TEXT_SECONDARY,TEXT_SECONDARY_DARK,)
CARD_ARROW = rx.color_mode_cond("#272361","#03A8C5",)


# ============================================================
# CARD DA META
# ============================================================

def meta_list_item(meta: rx.Var[MetaListItem],) -> rx.Component:
    """Card clicável de uma meta."""

    return rx.link(
        rx.hstack(
            rx.vstack(
                # ------------------------------------------------
                # Código
                # ------------------------------------------------

                rx.text(
                    "META ",
                    meta["codigo"],
                    color="#288140",
                    font_family=FONT_FAMILY_PRIMARY,
                    font_size="0.8rem",
                    font_weight="700",
                ),

                # ------------------------------------------------
                # Título
                # ------------------------------------------------

                rx.text(
                    meta["titulo"],
                    color=CARD_TEXT,
                    font_family=FONT_FAMILY_PRIMARY,
                    font_size="1rem",
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                    line_height="1.4",
                ),

                # ------------------------------------------------
                # Eixo
                # ------------------------------------------------

                rx.hstack(
                    rx.icon(
                        tag="layers",
                        size=14,
                        color=CARD_TEXT_SECONDARY,
                    ),

                    rx.text(
                        meta["eixo"],
                        color=CARD_TEXT_SECONDARY,
                        font_family=FONT_FAMILY_PRIMARY,
                        font_size="0.82rem",
                    ),

                    spacing="2",
                    align="center",
                ),
                align="start",
                spacing="2",
                flex="1",
                min_width="0",
            ),

            rx.center(
                rx.icon(
                    tag="chevron-right",
                    size=20,
                    color=CARD_ARROW,
                ),
                width="34px",
                height="34px",
                min_width="34px",
                border_radius="50%",
                background=rx.color_mode_cond("#F0F2F8","#202844",),
            ),
            align="center",
            width="100%",
            spacing="4",
        ),
        href=meta["url"],
        width="100%",
        padding="1rem 1.1rem",
        background=CARD_BACKGROUND,
        border=f"1px solid {CARD_BORDER}",
        border_radius="12px",
        text_decoration="none",
        cursor="pointer",
        transition=( "background 0.2s ease, " "border-color 0.2s ease, " "transform 0.2s ease"),
        _hover={"border_color": CARD_BORDER_HOVER,"background": CARD_BACKGROUND_HOVER,"transform": "translateY(-1px)",},
    )


# ============================================================
# ESTADO VAZIO
# ============================================================

def empty_result() -> rx.Component:
    """Mensagem exibida quando nenhum filtro encontra metas."""

    return rx.center(
        rx.vstack(
            rx.center(
                rx.icon(
                    tag="search-x",
                    size=22,
                    color=CARD_TEXT_SECONDARY,
                ),
                width="44px",
                height="44px",
                border_radius="50%",
                background=rx.color_mode_cond("#EEF3F7","#202844",),
            ),

            rx.text(
                "Nenhuma meta encontrada",
                color=CARD_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_weight=FONT_WEIGHT_SEMIBOLD,
            ),

            rx.text(
                "Tente alterar a pesquisa "
                "ou limpar os filtros.",
                color=CARD_TEXT_SECONDARY,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.85rem",
            ),
            spacing="2",
            align="center",
        ),
        width="100%",
        padding="3rem 1rem",
    )


# ============================================================
# RESULTADOS
# ============================================================

def meta_list_results() -> rx.Component:
    """Lista filtrada de metas."""

    return rx.vstack(
        rx.hstack(
            rx.text(MetaListState.metas_filtradas.length(),

                " meta(s) encontrada(s)",
                color=CARD_TEXT_SECONDARY,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.82rem",
            ),
            width="100%",
            align="center",
        ),

        rx.cond(MetaListState.metas_filtradas.length()> 0,
            rx.vstack(
                rx.foreach( MetaListState.metas_filtradas, meta_list_item, ),
                spacing="3",
                align="stretch",
                width="100%",
            ),
            empty_result(),
        ),
        spacing="3",
        align="stretch",
        width="100%",
    )


# ============================================================
# CONTEÚDO
# ============================================================

def meta_list_content() -> rx.Component:
    """Página de pesquisa e seleção das metas."""

    return rx.vstack(
        # Cabeçalho + filtros
        meta_filter_header(),
        # Conteúdo
        rx.cond(
            MetaListState.loading,
            rx.center(
                rx.vstack(
                    rx.spinner(
                        size="3",
                    ),
                    rx.text(
                        "Carregando metas...",
                        color=CARD_TEXT_SECONDARY,
                        font_family=FONT_FAMILY_PRIMARY,
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                padding="4rem 1rem",
            ),

            rx.cond(
                MetaListState.error_message != "",
                rx.box(
                    rx.hstack(
                        rx.icon(
                            tag="triangle-alert",
                            size=18,
                            color="#C62828",
                        ),

                        rx.text(
                            MetaListState.error_message,
                            color="#C62828",
                            font_family=FONT_FAMILY_PRIMARY,
                            font_size="0.9rem",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    width="100%",
                    padding="1rem",
                    background=rx.color_mode_cond( "rgba(198, 40, 40, 0.06)", "rgba(236, 32, 36, 0.10)",),
                    border_radius="10px",
                ),
                meta_list_results(),
            ),
        ),
        spacing="5",
        align="stretch",
        width="100%",
    )


# ============================================================
# PÁGINA
# ============================================================

def meta_list_page() -> rx.Component:
    """Página administrativa com a lista de metas."""

    return admin_layout(
        meta_list_content()
    )