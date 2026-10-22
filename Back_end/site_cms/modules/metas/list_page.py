import reflex as rx

from Back_end.interface.layouts.admin_layout import (
    admin_layout,
)
from Back_end.interface.theme.semantic import (
    BORDER,
    SURFACE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
)
from Back_end.site_cms.modules.metas.state import (
    MetaCmsState,
)


def _meta_row(
    meta,
) -> rx.Component:
    return rx.link(
        rx.box(
            rx.grid(
                rx.vstack(
                    rx.text(
                        "META",
                        color="#1281AA",
                        font_size="0.66rem",
                        font_weight="700",
                    ),
                    rx.text(
                        meta["codigo"],
                        color=TEXT_PRIMARY,
                        font_family=(
                            FONT_FAMILY_SECUNDARY
                        ),
                        font_size="1.2rem",
                    ),
                    spacing="1",
                    align="start",
                ),

                rx.vstack(
                    rx.text(
                        meta["titulo"],
                        color=TEXT_PRIMARY,
                        font_weight="600",
                        font_size="0.84rem",
                    ),
                    rx.text(
                        meta["eixo"],
                        color=TEXT_SECONDARY,
                        font_size="0.72rem",
                    ),
                    spacing="1",
                    align="start",
                ),

                rx.hstack(
                    rx.badge(
                        meta["status"],
                        variant="soft",
                        color_scheme=rx.cond(
                            meta["status"]
                            == "Publicado",
                            "green",
                            "orange",
                        ),
                    ),
                    rx.cond(
                        meta["conflitos"]
                        != "0",
                        rx.badge(
                            meta[
                                "conflitos"
                            ],
                            " conflito(s)",
                            color_scheme="red",
                            variant="soft",
                        ),
                        rx.badge(
                            "Sem conflitos",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    justify="end",
                    align="center",
                    spacing="2",
                ),

                columns={
                    "initial": "1",
                    "md": "3",
                },
                spacing="4",
                align_items="center",
                width="100%",
            ),
            width="100%",
            padding="1rem",
            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="10px",
            _hover={
                "transform": (
                    "translateY(-1px)"
                ),
                "box_shadow": (
                    "0 7px 18px "
                    "rgba(0,0,0,0.08)"
                ),
            },
            transition="all 0.18s ease",
        ),
        href=meta["url"],
        text_decoration="none",
        width="100%",
    )


def metas_cms_content() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text(
                    "SITE / METAS",
                    color="#1281AA",
                    font_size="0.72rem",
                    font_weight="700",
                    letter_spacing="0.08em",
                ),
                rx.heading(
                    "Fichas das Metas",
                    size="7",
                    color=TEXT_PRIMARY,
                    font_family=(
                        FONT_FAMILY_SECUNDARY
                    ),
                ),
                rx.text(
                    (
                        "Edite o conteúdo que será publicado no site. "
                        "Campos sincronizados com o SMAE continuam "
                        "personalizáveis no CMS."
                    ),
                    color=TEXT_SECONDARY,
                    font_family=(
                        FONT_FAMILY_PRIMARY
                    ),
                    font_size="0.86rem",
                ),
                spacing="2",
                align="start",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon(
                            tag="chart_no_axes_combined",
                            size=14,
                        ),
                        "Visão Geral",
                        background="#272361",
                        color="white",
                        cursor="pointer",
                    ),
                    href="/admin/site/metas/visao-geral",
                    text_decoration="none",
                ),
                rx.link(
                    rx.button(
                        rx.icon(
                            tag="arrow_left",
                            size=14,
                        ),
                        "Site",
                        variant="outline",
                        cursor="pointer",
                    ),
                    href="/admin/site",
                    text_decoration="none",
                ),
                spacing="2",
                align="center",
            ),
            width="100%",
            align="start",
        ),

        rx.input(
            placeholder=(
                "Buscar por número, título ou eixo..."
            ),
            value=MetaCmsState.search_text,
            on_change=(
                MetaCmsState
                .set_search_text
            ),
            width="100%",
            max_width="520px",
        ),

        rx.cond(
            MetaCmsState.list_error
            != "",
            rx.callout(
                MetaCmsState.list_error,
                icon="triangle_alert",
                color_scheme="red",
                width="100%",
            ),
            rx.box(),
        ),

        rx.cond(
            MetaCmsState.list_loading,
            rx.center(
                rx.spinner(
                    size="3"
                ),
                width="100%",
                min_height="250px",
            ),
            rx.vstack(
                rx.foreach(
                    MetaCmsState
                    .filtered_metas,
                    _meta_row,
                ),
                spacing="3",
                width="100%",
                align="stretch",
            ),
        ),

        spacing="5",
        width="100%",
        max_width="1180px",
        margin="0 auto",
        align="stretch",
        padding_bottom="5rem",
    )


def metas_cms_page() -> rx.Component:
    return admin_layout(
        metas_cms_content()
    )
