import reflex as rx

from Back_end.interface.layouts.admin_layout import (
    admin_layout,
)
from Back_end.interface.theme.semantic import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)
from Back_end.site_cms.modules.metas.components.detail import (
    action_bar,
    agencies_card,
    classification_card,
    conflict_dialog,
    initiatives_card,
    meta_cms_breadcrumb,
    meta_cms_hero,
    projection_card,
    regionalization_card,
    results_card,
    status_card,
)
from Back_end.site_cms.modules.metas.state import (
    MetaCmsState,
)


def _loading_view() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.spinner(
                size="3",
            ),
            rx.text(
                "Carregando ficha da Meta...",
                color=TEXT_SECONDARY,
                font_family=(
                    FONT_FAMILY_PRIMARY
                ),
                font_size="0.84rem",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
        min_height="340px",
    )


def _error_view() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.icon(
                tag="triangle_alert",
                size=24,
                color="#C62828",
            ),
            rx.heading(
                "Não foi possível abrir a Meta",
                size="5",
                color=TEXT_PRIMARY,
                font_family=(
                    FONT_FAMILY_SECUNDARY
                ),
            ),
            rx.text(
                MetaCmsState.error_message,
                color=TEXT_SECONDARY,
            ),
            rx.link(
                rx.button(
                    "Voltar para Metas",
                    variant="outline",
                ),
                href="/admin/site/metas",
                text_decoration="none",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
        min_height="340px",
    )


def _editor_content() -> rx.Component:
    return rx.vstack(
        meta_cms_breadcrumb(),

        meta_cms_hero(),

        rx.grid(
            status_card(),
            classification_card(),
            columns={
                "initial": "1",
                "xl": "2",
            },
            spacing="4",
            width="100%",
            align_items="stretch",
        ),

        rx.grid(
            projection_card(),
            agencies_card(),
            columns={
                "initial": "1",
                "xl": "2",
            },
            spacing="4",
            width="100%",
            align_items="stretch",
        ),

        initiatives_card(),

        results_card(),

        regionalization_card(),

        action_bar(),

        conflict_dialog(),

        spacing="4",
        width="100%",
        align="stretch",
        padding_bottom="5rem",
    )


def meta_cms_detail_content() -> rx.Component:
    return rx.cond(
        MetaCmsState.loading,
        _loading_view(),
        rx.cond(
            (
                MetaCmsState.error_message
                != ""
            )
            & (
                MetaCmsState
                .meta_content_id
                == None
            ),
            _error_view(),
            _editor_content(),
        ),
    )


def meta_cms_detail_page() -> rx.Component:
    return admin_layout(
        meta_cms_detail_content()
    )
