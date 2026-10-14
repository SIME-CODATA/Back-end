import reflex as rx

from Back_end.interface.layouts.admin_layout import (
    admin_layout,
)

from Back_end.interface.state.meta.meta_detail_state import (
    MetaDetailState,
)

from Back_end.interface.components.meta.detail.meta_breadcrumb import (
    meta_breadcrumb,
)

from Back_end.interface.components.meta.detail.meta_hero import (
    meta_hero,
)

from Back_end.interface.components.meta.detail.meta_status_card import (
    meta_status_card,
)

from Back_end.interface.components.meta.detail.meta_classification_card import (
    meta_classification_card,
)

from Back_end.interface.components.meta.detail.meta_budget_card import (
    meta_budget_card,
)

from Back_end.interface.components.meta.detail.meta_initiatives_card import (
    meta_initiatives_card,
)

from Back_end.interface.components.meta.detail.meta_regions_card import (
    meta_regions_card,
)

from Back_end.interface.components.meta.detail.meta_works_card import (
    meta_works_card,
)

from Back_end.interface.components.meta.detail.meta_projects_card import (
    meta_projects_card,
)

from Back_end.interface.components.meta.detail.meta_floating_actions import (
    meta_floating_actions,
)

from Back_end.interface.components.meta.detail.meta_search_panel import (
    meta_search_panel,
)

from Back_end.interface.components.meta.detail.meta_print_selector import (
    meta_print_selector,
)

from Back_end.interface.theme.semantic import (
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)


# ============================================================
# CORES
# ============================================================

PAGE_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

PAGE_MUTED = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)


# ============================================================
# CARREGAMENTO
# ============================================================

def loading_view() -> rx.Component:

    return rx.center(
        rx.vstack(
            rx.spinner(
                size="3",
            ),

            rx.text(
                "Carregando ficha da meta...",

                color=PAGE_MUTED,

                font_family=(
                    FONT_FAMILY_PRIMARY
                ),

                font_size="0.88rem",
            ),

            spacing="3",

            align="center",
        ),

        width="100%",

        min_height="320px",
    )


# ============================================================
# ERRO
# ============================================================

def error_view() -> rx.Component:

    return rx.center(
        rx.vstack(
            rx.center(
                rx.icon(
                    tag="triangle-alert",

                    size=22,

                    color="#C62828",
                ),

                width="46px",

                height="46px",

                border_radius="50%",

                background=rx.color_mode_cond(
                    "rgba(198, 40, 40, 0.08)",
                    "rgba(236, 32, 36, 0.12)",
                ),
            ),

            rx.text(
                "Não foi possível carregar "
                "a ficha",

                color=PAGE_TEXT,

                font_family=(
                    FONT_FAMILY_SECUNDARY
                ),

                font_size="1.2rem",
            ),

            rx.text(
                MetaDetailState.error_message,

                color=PAGE_MUTED,

                font_family=(
                    FONT_FAMILY_PRIMARY
                ),

                font_size="0.84rem",
            ),

            rx.link(
                rx.button(
                    "VOLTAR PARA METAS",

                    background="#272361",

                    color="white",

                    font_family=(
                        FONT_FAMILY_SECUNDARY
                    ),

                    cursor="pointer",
                ),

                href="/admin/metas",

                text_decoration="none",
            ),

            spacing="3",

            align="center",
        ),

        width="100%",

        min_height="320px",
    )


# ============================================================
# NÃO ENCONTRADA
# ============================================================

def not_found_view() -> rx.Component:

    return rx.center(
        rx.vstack(
            rx.center(
                rx.icon(
                    tag="file-question",

                    size=22,

                    color=PAGE_MUTED,
                ),

                width="46px",

                height="46px",

                border_radius="50%",

                background=rx.color_mode_cond(
                    "#EEF3F7",
                    "#202844",
                ),
            ),

            rx.text(
                "Meta não encontrada",

                color=PAGE_TEXT,

                font_family=(
                    FONT_FAMILY_SECUNDARY
                ),

                font_size="1.2rem",
            ),

            rx.text(
                "Não encontramos a META ",

                MetaDetailState.codigo_atual,

                ".",

                color=PAGE_MUTED,

                font_family=(
                    FONT_FAMILY_PRIMARY
                ),

                font_size="0.84rem",
            ),

            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon(
                            tag="arrow-left",
                            size=15,
                        ),

                        "LISTA DE METAS",

                        variant="outline",

                        cursor="pointer",
                    ),

                    href="/admin/metas",

                    text_decoration="none",
                ),

                rx.button(
                    rx.icon(
                        tag="search",
                        size=15,
                    ),

                    "BUSCAR META",

                    on_click=(
                        MetaDetailState
                        .open_search
                    ),

                    background="#272361",

                    color="white",

                    cursor="pointer",
                ),

                spacing="3",
            ),

            spacing="3",

            align="center",
        ),

        width="100%",

        min_height="320px",
    )


# ============================================================
# FICHA
# ============================================================

def ficha_content() -> rx.Component:
    """Conteúdo completo da Ficha da Meta."""

    return rx.vstack(

        meta_breadcrumb(),

        meta_hero(),

        # ----------------------------------------------------
        # Status + classificações
        # ----------------------------------------------------

        rx.grid(
            meta_status_card(),

            meta_classification_card(),

            columns={
                "initial": "1",
                "xl": "2",
            },

            spacing="4",

            width="100%",

            align_items="stretch",
        ),

        # ----------------------------------------------------
        # Orçamento + regionalização
        # ----------------------------------------------------

        rx.grid(
            meta_budget_card(),

            meta_regions_card(),

            columns={
                "initial": "1",
                "xl": "2",
            },

            spacing="4",

            width="100%",

            align_items="stretch",
        ),

        meta_initiatives_card(),

        meta_works_card(),

        meta_projects_card(),

        spacing="4",

        align="stretch",

        width="100%",

        padding_bottom="5rem",
    )


# ============================================================
# CONTEÚDO
# ============================================================

def meta_detail_content() -> rx.Component:

    return rx.box(
        meta_search_panel(),
        meta_print_selector(),
        meta_floating_actions(),

        rx.cond(
            MetaDetailState.loading,

            loading_view(),

            rx.cond(
                MetaDetailState.error_message
                != "",

                error_view(),

                rx.cond(
                    MetaDetailState
                    .ficha_encontrada,

                    ficha_content(),

                    not_found_view(),
                ),
            ),
        ),

        width="100%",
    )


# ============================================================
# PÁGINA
# ============================================================

def meta_detail_page() -> rx.Component:

    return admin_layout(
        meta_detail_content()
    )