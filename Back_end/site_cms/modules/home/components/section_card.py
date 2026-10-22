import reflex as rx


CARD_BG = rx.color_mode_cond(
    "#FFFFFF",
    "#18243E",
)

CARD_BORDER = rx.color_mode_cond(
    "rgba(22, 37, 63, 0.10)",
    "rgba(255, 255, 255, 0.10)",
)

TEXT_PRIMARY = rx.color_mode_cond(
    "#1B263B",
    "#F4F7FF",
)

TEXT_MUTED = rx.color_mode_cond(
    "#6C7890",
    "#B8C4DA",
)


def _status_badge(section) -> rx.Component:
    return rx.cond(
        section["has_draft"] == "true",
        rx.box(
            rx.text(
                "Rascunho",
                font_size="0.72rem",
                font_weight="600",
            ),
            padding="0.25rem 0.55rem",
            border_radius="999px",
            background="#FFF3CD",
            color="#7A5B00",
        ),
        rx.box(
            rx.text(
                "Publicado",
                font_size="0.72rem",
                font_weight="600",
            ),
            padding="0.25rem 0.55rem",
            border_radius="999px",
            background="#DCFCE7",
            color="#166534",
        ),
    )


def section_card(section) -> rx.Component:
    """Card visual de uma seção da Página Inicial."""

    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon(
                    tag="layout_panel_top",
                    size=19,
                    color="#FFFFFF",
                ),
                width="42px",
                min_width="42px",
                height="42px",
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="11px",
                background="#1281AA",
            ),

            rx.vstack(
                rx.hstack(
                    rx.heading(
                        section["name"],
                        size="4",
                        color=TEXT_PRIMARY,
                    ),
                    _status_badge(section),
                    align="center",
                    spacing="3",
                    wrap="wrap",
                ),
                rx.text(
                    section["description"],
                    color=TEXT_MUTED,
                    font_size="0.78rem",
                ),
                rx.text(
                    section["summary"],
                    color=TEXT_PRIMARY,
                    font_size="0.86rem",
                    line_height="1.5",
                    max_width="760px",
                ),
                rx.hstack(
                    rx.text(
                        section["source_label"],
                        color=TEXT_MUTED,
                        font_size="0.72rem",
                    ),
                    rx.text(
                        "•",
                        color=TEXT_MUTED,
                        font_size="0.72rem",
                    ),
                    rx.text(
                        rx.cond(
                            section["enabled"] == "true",
                            "Visível no site",
                            "Oculta",
                        ),
                        color=TEXT_MUTED,
                        font_size="0.72rem",
                    ),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                spacing="2",
                align="start",
                flex="1",
            ),

            rx.spacer(),

            rx.link(
                rx.button(
                    rx.icon(
                        tag="pencil",
                        size=15,
                    ),
                    "Editar",
                    size="2",
                    variant="soft",
                    cursor="pointer",
                ),
                href=section["editor_href"],
                text_decoration="none",
            ),

            width="100%",
            align="center",
            spacing="4",
        ),
        width="100%",
        padding="1rem 1.1rem",
        background=CARD_BG,
        border=f"1px solid {CARD_BORDER}",
        border_radius="14px",
        box_shadow=rx.color_mode_cond(
            "0 7px 24px rgba(28, 45, 75, 0.05)",
            "0 7px 24px rgba(0, 0, 0, 0.12)",
        ),
    )
