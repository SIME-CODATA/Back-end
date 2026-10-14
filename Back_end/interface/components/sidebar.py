import reflex as rx

from Back_end.interface.state.sidebar_state import SidebarState
from Back_end.interface.theme.typography import FONT_FAMILY_PRIMARY
from Back_end.interface.theme.semantic import ( PAGE_BACKGROUND, PAGE_BACKGROUND_DARK, TEXT_PRIMARY, TEXT_PRIMARY_DARK)


# ============================================================
# IDENTIDADE VISUAL
# ============================================================

MENU_BACKGROUND = rx.color_mode_cond( PAGE_BACKGROUND, PAGE_BACKGROUND_DARK ),
MENU_BACKGROUND_HOVER = rx.color_mode_cond("#1281aa82","#344D86")
MENU_BACKGROUND_ACTIVE = rx.color_mode_cond ("#1281aa82", "#3A5794")

MENU_TEXT = rx.color_mode_cond( TEXT_PRIMARY, TEXT_PRIMARY_DARK ),
MENU_TEXT_MUTED = rx.color_mode_cond("#74819b","#D4DDF1")

MENU_BORDER = rx.color_mode_cond("rgba(98, 98, 146, 0.12)","rgba(255, 255, 255, 0.12)")

MENU_WIDTH_OPEN = "280px"
MENU_WIDTH_CLOSED = "76px"


# ============================================================
# MARCA
# ============================================================


def color_mode_button() -> rx.Component:
    """Botão para alternar entre tema claro e escuro."""

    return rx.color_mode.button(
        background= rx.color_mode_cond("rgba(0, 0, 0, 0.10)", "rgba(183, 183, 183, 0.10)"),
        color=MENU_TEXT,
        border= rx.color_mode_cond("1px solid rgba(39, 35, 97, 0.12)", "1px solid rgba(255, 255, 255, 0.12)"),
        border_radius="8px",
        padding="0.45rem",
        min_width="34px",
        width="34px",
        height="34px",
        cursor="pointer",

        _hover={
            "background": "rgba(255, 255, 255, 0.18)",
        },
    )


def sidebar_logo() -> rx.Component:
    """Exibe a logo correspondente ao estado da sidebar."""

    return rx.cond(
        SidebarState.expanded,

        rx.image(
            src="/svg/logo_PdM_Completo_colorido.svg",
            width="155px",
            height="auto",
            object_fit="contain",
            
            filter=rx.color_mode_cond(
                "none",
                "brightness(0) invert(1)",
            ),

            transition="filter 0.2s ease",
        ),

        rx.image(
            src="/svg/prog_metas_log.svg",
            width="34px",
            height="34px",
            object_fit="contain",
            
            filter=rx.color_mode_cond(
                "none",
                "brightness(0) invert(1)",
            ),

            transition="filter 0.2s ease",
        ),
    )


def sidebar_toggle() -> rx.Component:
    """Botão para expandir ou recolher a navegação."""

    return rx.button(
        rx.cond(
            SidebarState.expanded,
            rx.icon( tag="panel_left_close", size=18,),
            rx.icon( tag="panel_left_open", size=18,),
        ),

        on_click=SidebarState.toggle_sidebar,

        background="transparent",
        color=MENU_TEXT,
        padding="0.4rem",
        min_width="auto",
        height="auto",
        cursor="pointer",
        border_radius="6px",

        _hover={
            "background": MENU_BACKGROUND_HOVER,
        },
    )


def sidebar_header() -> rx.Component:
    """Cabeçalho adaptável aos estados aberto e recolhido."""

    return rx.box(
        rx.cond(
            SidebarState.expanded,

            # SIDEBAR ABERTA
            rx.hstack( color_mode_button(), sidebar_logo(), rx.spacer(), sidebar_toggle(), width="100%", align="center", spacing="3", ),

            # SIDEBAR FECHADA
            rx.vstack(
                sidebar_logo(),
                rx.hstack( color_mode_button(), sidebar_toggle(), align="center", justify="center", spacing="2",),
                align="center",
                spacing="3",
                width="100%",
            ),
        ),
        width="100%",
        padding=rx.cond( SidebarState.expanded, "1.25rem 0.85rem", "1rem 0.25rem", ),
        border_bottom=f"1px solid {MENU_BORDER}",
    )


# ============================================================
# PESQUISA DO MENU
# ============================================================

def sidebar_search() -> rx.Component:
    """Pesquisa os itens de navegação."""

    return rx.cond(
        SidebarState.expanded,

        rx.box(
            rx.input(
                rx.input.slot(
                    rx.icon(
                        tag="search",
                        size=15,
                        color=MENU_TEXT_MUTED,
                    ),
                ),

                placeholder="Filtrar menus",
                value=SidebarState.filter_text,
                on_change=SidebarState.update_filter,

                width="100%",
                size="1",
                variant="soft",

                background= rx.color_mode_cond( "#F7F9FC", "#20335F" ),
                color=MENU_TEXT,
                border=f"1px solid {MENU_BORDER}",
                border_radius="8px",
            ),

            padding="0.85rem 0.9rem",
            border_bottom=f"1px solid {MENU_BORDER}",
        ),

        rx.box(),
    )


# ============================================================
# ITENS COM PÁGINA IMPLEMENTADA
# ============================================================

def sidebar_link(
    icon: str,
    label: str,
    href: str,
    active,
) -> rx.Component:
    """Item de menu com uma rota existente."""

    return rx.link(
        rx.hstack(
            rx.icon(
                tag=icon,
                size=19,
                color=MENU_TEXT,
            ),

            rx.cond(
                SidebarState.expanded,

                rx.text(
                    label,
                    color=MENU_TEXT,
                    font_size="0.88rem",
                    font_weight="500",
                    white_space="nowrap",
                ),
            ),

            align="center",
            spacing="3",
            width="100%",
            justify=rx.cond(
                SidebarState.expanded,
                "start",
                "center",
            ),
        ),

        href=href,
        title=label,

        width="100%",
        padding=rx.cond(
            SidebarState.expanded,
            "0.75rem 0.85rem",
            "0.75rem 0.4rem",
        ),

        background=rx.cond(
            active,
            MENU_BACKGROUND_ACTIVE,
            "transparent",
        ),

        border_radius="8px",
        text_decoration="none",
        cursor="pointer",

        _hover={
            "background": MENU_BACKGROUND_HOVER,
        },
    )


# ============================================================
# ITENS RESERVADOS PARA FUTURAS FUNCIONALIDADES
# ============================================================

def sidebar_future_item(
    icon: str,
    label: str,
) -> rx.Component:
    """Item visível, mas ainda sem página implementada."""

    return rx.hstack(
        rx.icon(
            tag=icon,
            size=19,
            color=MENU_TEXT_MUTED,
        ),

        rx.cond(
            SidebarState.expanded,

            rx.hstack(
                rx.text(
                    label,
                    color=MENU_TEXT_MUTED,
                    font_size="0.85rem",
                ),

                rx.spacer(),

                rx.text(
                    "Em breve",
                    color="#B5C5E8",
                    font_size="0.62rem",
                    white_space="nowrap",
                ),

                width="100%",
                align="center",
            ),
        ),

        width="100%",
        align="center",
        spacing="3",

        padding=rx.cond(
            SidebarState.expanded,
            "0.75rem 0.85rem",
            "0.75rem 0.4rem",
        ),

        justify=rx.cond(
            SidebarState.expanded,
            "start",
            "center",
        ),

        opacity="0.75",
        cursor="not-allowed",
        border_radius="8px",
    )


# ============================================================
# GRUPO SITE
# ============================================================

def site_menu_button() -> rx.Component:
    """Abre e recolhe os submenus da administração do site."""

    return rx.button(
        rx.hstack(
            rx.icon(
                tag="globe",
                size=19,
                color=MENU_TEXT,
            ),

            rx.cond(
                SidebarState.expanded,

                rx.hstack(
                    rx.text(
                        "Site",
                        color=MENU_TEXT,
                        font_size="0.88rem",
                        font_weight="500",
                    ),

                    rx.spacer(),

                    rx.cond(
                        SidebarState.show_site_children,

                        rx.icon(
                            tag="chevron_down",
                            size=15,
                            color=MENU_TEXT_MUTED,
                        ),

                        rx.icon(
                            tag="chevron_right",
                            size=15,
                            color=MENU_TEXT_MUTED,
                        ),
                    ),

                    width="100%",
                    align="center",
                ),
            ),

            align="center",
            spacing="3",
            width="100%",

            justify=rx.cond(
                SidebarState.expanded,
                "start",
                "center",
            ),
        ),

        on_click=SidebarState.toggle_site,

        title="Site",
        width="100%",

        padding=rx.cond(
            SidebarState.expanded,
            "0.75rem 0.85rem",
            "0.75rem 0.4rem",
        ),

        height="auto",
        min_width="auto",
        background="transparent",
        border_radius="8px",
        cursor="pointer",

        _hover={
            "background": MENU_BACKGROUND_HOVER,
        },
    )


def site_submenu_item(label: str) -> rx.Component:
    """Submenu reservado para futura edição manual do site."""

    return rx.hstack(
        rx.box(
            width="5px",
            height="5px",
            min_width="5px",
            border_radius="50%",
            background="#9FB0D3",
        ),

        rx.text(
            label,
            color=MENU_TEXT_MUTED,
            font_size="0.82rem",
            white_space="normal",
        ),

        align="center",
        spacing="3",
        width="100%",
        padding="0.6rem 0.65rem",
        border_radius="6px",
        opacity="0.8",
        cursor="not-allowed",
        title="Página ainda não implementada",
    )


def site_submenu() -> rx.Component:
    """Submenus que organizarão os conteúdos manuais do site."""

    return rx.cond(
        SidebarState.show_site_children,

        rx.vstack(
            rx.cond(
                SidebarState.visible_items["site_home"],
                site_submenu_item("Página inicial"),
            ),

            rx.cond(
                SidebarState.visible_items["site_news"],
                site_submenu_item("Notícias"),
            ),

            rx.cond(
                SidebarState.visible_items["site_about"],
                site_submenu_item("Sobre"),
            ),

            rx.cond(
                SidebarState.visible_items["site_history"],
                site_submenu_item("Histórico"),
            ),

            rx.cond(
                SidebarState.visible_items["site_participation"],
                site_submenu_item("Participação Social"),
            ),

            rx.cond(
                SidebarState.visible_items["site_metas"],
                site_submenu_item("Metas"),
            ),

            rx.cond(
                SidebarState.visible_items["site_regionalization"],
                site_submenu_item("Regionalização"),
            ),

            rx.cond(
                SidebarState.visible_items["site_transparency"],
                site_submenu_item(
                    "Transparência e Monitoramento"
                ),
            ),

            spacing="0",
            align="stretch",
            width="100%",
            padding_left="1.5rem",
            padding_right="0.25rem",
            padding_bottom="0.5rem",
        ),

        rx.box(),
    )


# ============================================================
# NAVEGAÇÃO COMPLETA
# ============================================================

def sidebar_navigation() -> rx.Component:
    """Organização completa dos menus do PDM V2.0."""

    return rx.vstack(
        rx.cond(
            SidebarState.visible_items["overview"],

            sidebar_link(
                icon="layout_dashboard",
                label="Visão Geral",
                href="/admin",
                active=SidebarState.overview_active,
            ),
        ),

        rx.cond(
            SidebarState.visible_items["metas"],

            sidebar_link(
                icon="target",
                label="Metas",
                href="/admin/metas",
                active=SidebarState.metas_active,
            ),
        ),

        rx.cond(
            SidebarState.visible_items["upload"],

            sidebar_future_item(
                icon="file_up",
                label="Upload de Arquivos",
            ),
        ),

        rx.cond(
            SidebarState.visible_items["export"],

            sidebar_future_item(
                icon="file_down",
                label="Export de Arquivos",
            ),
        ),

        rx.cond(
            SidebarState.visible_items["site"],

            rx.vstack(
                site_menu_button(),
                site_submenu(),

                spacing="0",
                align="stretch",
                width="100%",
            ),
        ),

        rx.cond(
            SidebarState.visible_items["images"],

            sidebar_future_item(
                icon="image",
                label="Banco de imagem",
            ),
        ),

        rx.cond(
            SidebarState.visible_items["users"],

            sidebar_future_item(
                icon="users",
                label="Usuários",
            ),
        ),

        rx.cond(
            SidebarState.has_visible_items == False,

            rx.cond(
                SidebarState.expanded,

                rx.text(
                    "Nenhum menu encontrado.",
                    color=MENU_TEXT_MUTED,
                    font_size="0.8rem",
                    padding="0.75rem",
                ),
            ),
        ),

        width="100%",
        align="stretch",
        spacing="1",
    )


# ============================================================
# SIDEBAR PRINCIPAL
# ============================================================

def sidebar() -> rx.Component:
    """Sidebar administrativa"""

    return rx.box(
        rx.vstack(
            sidebar_header(),

            sidebar_search(),

            # Área independente de rolagem.
            rx.box(
                sidebar_navigation(),

                width="100%",
                flex="1",
                min_height="0",
                overflow_y="auto",
                overflow_x="hidden",
                padding="0.85rem 0.65rem",
            ),

            width="90%",
            height="100%",
            spacing="0",
            align="stretch",
        ),

        background=MENU_BACKGROUND,
        border_top_right_radius="20px",
        border_bottom_right_radius="15px",

        width=rx.cond(
            SidebarState.expanded,
            MENU_WIDTH_OPEN,
            MENU_WIDTH_CLOSED,
        ),

        min_width=rx.cond(
            SidebarState.expanded,
            MENU_WIDTH_OPEN,
            MENU_WIDTH_CLOSED,
        ),

        height="96vh",
        overflow="hidden",
        margin_top="1rem",
        margin_bottom="1rem",
        box_shadow="3px 3px 13px -10px rgba(255, 255, 255, 0.65)",

        font_family=FONT_FAMILY_PRIMARY,

        transition=(
            "width 0.25s ease, "
            "min-width 0.25s ease"
        ),
    )