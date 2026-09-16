import reflex as rx

from Back_end.interface.state.sidebar_state import SidebarState
from Back_end.interface.theme.semantic import (
    SIDEBAR_ACCENT,
    SIDEBAR_BACKGROUND,
    SIDEBAR_BACKGROUND_ACTIVE,
    SIDEBAR_TEXT,
    SIDEBAR_TEXT_MUTED,
)
from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_SIZE_SM,
    FONT_WEIGHT_MEDIUM,
    FONT_WEIGHT_SEMIBOLD,
)


def sidebar_item(
    icon: str,
    label: str,
    href: str,
) -> rx.Component:
    """Item de navegação da barra lateral."""

    return rx.link(
        rx.hstack(
            rx.icon(
                tag=icon,
                size=20,
                color=SIDEBAR_TEXT_MUTED,
            ),
            rx.cond(
                SidebarState.expanded,
                rx.text(
                    label,
                    font_size=FONT_SIZE_SM,
                    font_weight=FONT_WEIGHT_MEDIUM,
                    color=SIDEBAR_TEXT,
                    white_space="nowrap",
                ),
            ),
            width="100%",
            align="center",
            spacing="3",
        ),
        href=href,
        width="100%",
        padding="0.75rem 1rem",
        border_radius="8px",
        text_decoration="none",
        transition="all 0.2s ease",
        _hover={
            "background": SIDEBAR_BACKGROUND_ACTIVE,
        },
    )


def sidebar_brand() -> rx.Component:
    """Identificação visual do Programa de Metas."""

    return rx.hstack(
        rx.center(
            rx.text(
                "SP",
                color=SIDEBAR_BACKGROUND,
                font_weight="700",
                font_size="0.8rem",
            ),
            width="38px",
            height="38px",
            border_radius="50%",
            background=SIDEBAR_ACCENT,
            flex_shrink="0",
        ),
        rx.cond(
            SidebarState.expanded,
            rx.vstack(
                rx.text(
                    "PROGRAMA DE METAS",
                    color=SIDEBAR_TEXT,
                    font_size="0.78rem",
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                    letter_spacing="0.04em",
                    white_space="nowrap",
                ),
                rx.text(
                    "2025–2028",
                    color=SIDEBAR_ACCENT,
                    font_size="0.72rem",
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                ),
                spacing="0",
                align="start",
            ),
        ),
        width="100%",
        align="center",
        spacing="3",
    )


def sidebar_toggle() -> rx.Component:
    """Botão que expande ou recolhe a sidebar."""

    return rx.button(
        rx.cond(
            SidebarState.expanded,
            rx.icon(
                tag="panel_left_close",
                size=18,
            ),
            rx.icon(
                tag="panel_left_open",
                size=18,
            ),
        ),
        on_click=SidebarState.toggle_sidebar,
        background="transparent",
        color=SIDEBAR_TEXT_MUTED,
        padding="0.5rem",
        min_width="auto",
        height="auto",
        cursor="pointer",
        border_radius="8px",
        _hover={
            "background": SIDEBAR_BACKGROUND_ACTIVE,
            "color": SIDEBAR_TEXT,
        },
    )


def sidebar() -> rx.Component:
    """Barra lateral principal da interface administrativa."""

    return rx.box(
        rx.vstack(
            # Logo + recolher
            rx.hstack(
                sidebar_brand(),
                sidebar_toggle(),
                width="100%",
                justify="between",
                align="center",
            ),

            rx.divider(
                border_color="rgba(255, 255, 255, 0.10)",
                width="100%",
            ),

            # Navegação
            rx.vstack(
                sidebar_item(
                    icon="layout_dashboard",
                    label="Visão Geral",
                    href="/admin",
                ),
                sidebar_item(
                    icon="target",
                    label="Metas",
                    href="/admin/metas",
                ),
                sidebar_item(
                    icon="refresh_cw",
                    label="Integrações",
                    href="/admin/integracoes",
                ),
                sidebar_item(
                    icon="upload",
                    label="Importações",
                    href="/admin/importacoes",
                ),
                sidebar_item(
                    icon="file_text",
                    label="Relatórios",
                    href="/admin/relatorios",
                ),
                sidebar_item(
                    icon="users",
                    label="Usuários",
                    href="/admin/usuarios",
                ),
                sidebar_item(
                    icon="settings",
                    label="Configurações",
                    href="/admin/configuracoes",
                ),
                width="100%",
                spacing="1",
                align="stretch",
            ),

            rx.spacer(),

            # Rodapé da sidebar
            rx.divider(
                border_color="rgba(255, 255, 255, 0.10)",
                width="100%",
            ),

            sidebar_item(
                icon="log_out",
                label="Sair",
                href="/logout",
            ),

            width="100%",
            height="100%",
            align="stretch",
            spacing="4",
        ),
        background=SIDEBAR_BACKGROUND,
        width=rx.cond(
            SidebarState.expanded,
            "260px",
            "76px",
        ),
        min_width=rx.cond(
            SidebarState.expanded,
            "260px",
            "76px",
        ),
        height="100vh",
        padding="1rem",
        transition="width 0.25s ease, min-width 0.25s ease",
        font_family=FONT_FAMILY_PRIMARY,
        overflow="hidden",
    )