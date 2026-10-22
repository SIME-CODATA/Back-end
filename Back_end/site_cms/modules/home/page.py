import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.site_cms.modules.home.components.section_card import section_card
from Back_end.site_cms.modules.home.state import HomeCmsState


TEXT_PRIMARY = rx.color_mode_cond(
    "#1B263B",
    "#F4F7FF",
)

TEXT_MUTED = rx.color_mode_cond(
    "#6C7890",
    "#B8C4DA",
)

PANEL_BG = rx.color_mode_cond(
    "#F7F9FC",
    "#111A2E",
)


def _summary_box(
    label: str,
    value,
    icon: str,
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(
                tag=icon,
                size=18,
                color="#1281AA",
            ),
            rx.vstack(
                rx.text(
                    value,
                    font_size="1.15rem",
                    font_weight="700",
                    color=TEXT_PRIMARY,
                ),
                rx.text(
                    label,
                    font_size="0.72rem",
                    color=TEXT_MUTED,
                ),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        padding="0.8rem 1rem",
        background=PANEL_BG,
        border_radius="12px",
        min_width="150px",
    )


def home_cms_content() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.link(
                rx.hstack(
                    rx.icon(
                        tag="arrow_left",
                        size=14,
                    ),
                    rx.text(
                        "Site",
                        font_size="0.78rem",
                    ),
                    spacing="2",
                    align="center",
                ),
                href="/admin/site",
                color="#1281AA",
                text_decoration="none",
            ),
            rx.text(
                "PÁGINA INICIAL",
                font_size="0.76rem",
                font_weight="700",
                letter_spacing="0.12em",
                color="#1281AA",
            ),
            rx.heading(
                "Página Inicial",
                size="7",
                color=TEXT_PRIMARY,
            ),
            rx.text(
                (
                    "Todos os módulos da Home ficam centralizados aqui. "
                    "Entre em cada bloco para editar o conteúdo correspondente."
                ),
                color=TEXT_MUTED,
                font_size="0.95rem",
            ),
            spacing="2",
            align="start",
            width="100%",
        ),

        rx.hstack(
            _summary_box(
                "Módulos",
                HomeCmsState.section_count,
                "layout_panel_top",
            ),
            _summary_box(
                "Publicados",
                HomeCmsState.published_count,
                "circle_check",
            ),
            _summary_box(
                "Rascunhos",
                HomeCmsState.draft_count,
                "file_pen_line",
            ),
            spacing="3",
            wrap="wrap",
            width="100%",
        ),

        rx.cond(
            HomeCmsState.error_message != "",
            rx.callout(
                HomeCmsState.error_message,
                icon="triangle_alert",
                color_scheme="red",
                width="100%",
            ),
            rx.box(),
        ),

        rx.cond(
            HomeCmsState.loading,
            rx.box(
                rx.vstack(
                    rx.spinner(
                        size="3",
                    ),
                    rx.text(
                        "Carregando conteúdo da Página Inicial...",
                        color=TEXT_MUTED,
                    ),
                    spacing="3",
                    align="center",
                ),
                width="100%",
                padding="3rem",
            ),
            rx.cond(
                HomeCmsState.section_count == 0,
                rx.box(
                    rx.text(
                        "Nenhum módulo cadastrado para a Página Inicial.",
                        color=TEXT_MUTED,
                    ),
                    width="100%",
                    padding="2rem",
                    text_align="center",
                ),
                rx.vstack(
                    rx.foreach(
                        HomeCmsState.sections,
                        section_card,
                    ),
                    spacing="3",
                    width="100%",
                ),
            ),
        ),

        width="100%",
        max_width="1180px",
        margin="0 auto",
        spacing="6",
        align="stretch",
    )


def site_cms_home_page() -> rx.Component:
    return admin_layout(
        home_cms_content()
    )
