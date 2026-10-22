import reflex as rx

from Back_end.site_cms.modules.metas.state import (
    MetaCmsState,
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


def source_badge(
    source,
) -> rx.Component:
    return rx.badge(
        source,
        variant="soft",
        color_scheme=rx.cond(
            source == "SMAE",
            "blue",
            rx.cond(
                source
                == "Personalizado",
                "orange",
                "gray",
            ),
        ),
        size="1",
    )


def field_header(
    label: str,
    source,
    field_key: str,
) -> rx.Component:
    return rx.hstack(
        rx.text(
            label,
            color=TEXT_PRIMARY,
            font_family=(
                FONT_FAMILY_PRIMARY
            ),
            font_size="0.78rem",
            font_weight="600",
        ),
        source_badge(
            source
        ),
        rx.spacer(),
        rx.cond(
            source
            == "Personalizado",
            rx.button(
                rx.icon(
                    tag="refresh_ccw",
                    size=12,
                ),
                "Usar SMAE",
                size="1",
                variant="ghost",
                on_click=lambda: (
                    MetaCmsState
                    .restore_field_from_smae(
                        field_key
                    )
                ),
                cursor="pointer",
            ),
            rx.box(),
        ),
        width="100%",
        align="center",
        spacing="2",
    )


def text_input(
    *,
    label: str,
    source,
    field_key: str,
    value,
    on_change,
    placeholder: str = "",
) -> rx.Component:
    return rx.vstack(
        field_header(
            label,
            source,
            field_key,
        ),
        rx.input(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            width="100%",
        ),
        spacing="2",
        width="100%",
        align="stretch",
    )


def textarea_input(
    *,
    label: str,
    source,
    field_key: str,
    value,
    on_change,
    placeholder: str = "",
    min_height: str = "120px",
) -> rx.Component:
    return rx.vstack(
        field_header(
            label,
            source,
            field_key,
        ),
        rx.text_area(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            width="100%",
            min_height=min_height,
            resize="vertical",
        ),
        spacing="2",
        width="100%",
        align="stretch",
    )


def cms_card(
    title: str,
    *children,
    description: str = "",
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.heading(
                    title,
                    size="4",
                    color=TEXT_PRIMARY,
                    font_family=(
                        FONT_FAMILY_SECUNDARY
                    ),
                ),
                rx.cond(
                    description != "",
                    rx.text(
                        description,
                        color=TEXT_SECONDARY,
                        font_family=(
                            FONT_FAMILY_PRIMARY
                        ),
                        font_size="0.76rem",
                    ),
                    rx.box(),
                ),
                spacing="1",
                align="start",
            ),
            *children,
            spacing="4",
            align="stretch",
            width="100%",
        ),
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        padding="1.2rem",
        width="100%",
    )
