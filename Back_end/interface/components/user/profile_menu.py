import reflex as rx

from Back_end.access.states.auth_state import (AuthState,)
from Back_end.interface.state.dashboard_state import (DashboardState,)
from Back_end.interface.theme.semantic import (BORDER,BORDER_DARK,TEXT_PRIMARY,TEXT_PRIMARY_DARK,TEXT_SECONDARY,TEXT_SECONDARY_DARK,)
from Back_end.interface.theme.typography import (FONT_FAMILY_PRIMARY,FONT_SIZE_SM,FONT_WEIGHT_MEDIUM,FONT_WEIGHT_SEMIBOLD,)

# ============================================================
# CORES
# ============================================================

def profile_primary_text(): return rx.color_mode_cond( TEXT_PRIMARY, TEXT_PRIMARY_DARK, )

def profile_secondary_text(): return rx.color_mode_cond(  TEXT_SECONDARY,  TEXT_SECONDARY_DARK, )

def profile_border(): return rx.color_mode_cond( BORDER, BORDER_DARK, )
PROFILE_BACKGROUND = rx.color_mode_cond("#FFFFFF","#1E2948",)
PROFILE_HOVER = rx.color_mode_cond("#F4F7FA","#2B3C68",)

# ============================================================
# AVATAR
# ============================================================

def profile_avatar(size: str = "36px",) -> rx.Component:
    """Avatar padrão do usuário."""

    return rx.center(
        rx.icon(tag="user", size=17, color="white",),
        width=size, height=size, min_width=size, border_radius="50%", background="#272361",
    )


# ============================================================
# ITEM NORMAL
# ============================================================

def profile_menu_item(icon: str,label: str,on_select=None,) -> rx.Component:
    """Item clicável do painel do perfil."""

    return rx.dropdown_menu.item(
        rx.hstack(
            rx.icon(tag=icon,size=16,),
            rx.text(label,font_size="0.82rem",),
            spacing="3", align="center",
        ),
        on_select=on_select, cursor="pointer",
    )


# ============================================================
# ITEM FUTURO
# ============================================================

def profile_future_item(icon: str,label: str,) -> rx.Component:
    """Item planejado, ainda não implementado."""

    return rx.dropdown_menu.item(
        rx.hstack(
            rx.icon(tag=icon,size=16,),
            rx.text(label,font_size="0.82rem",),
            rx.spacer(),
            rx.text("Em breve", font_size="0.62rem", color=profile_secondary_text(),),
            width="100%", align="center", spacing="3",
        ),
        disabled=True,
    )


# ============================================================
# INFORMAÇÕES DO USUÁRIO
# ============================================================

def profile_menu_header() -> rx.Component:
    """Resumo do usuário dentro do dropdown."""

    return rx.vstack(
        rx.hstack( profile_avatar("42px"),
            rx.vstack(
                rx.text( AuthState.current_user_name, color=profile_primary_text(), font_size="0.86rem", font_weight=(FONT_WEIGHT_SEMIBOLD),),
                rx.text( AuthState.current_user_email, color=profile_secondary_text(), font_size="0.7rem",),
                spacing="0", align="start",
            ),
            width="100%", align="center", spacing="3",
        ),

        rx.hstack(
            rx.icon(tag="shield_check", size=13, color="#1287B2",),
            rx.text(AuthState.current_role_label, color="#1287B2", font_size="0.68rem", font_weight=(FONT_WEIGHT_SEMIBOLD),),
            background=rx.color_mode_cond( "rgba(18, 135, 178, 0.08)", "rgba(76, 199, 226, 0.10)",), padding="0.3rem 0.55rem", border_radius="999px", width="fit-content", align="center", spacing="2",
        ),
        width="100%", spacing="3", padding="0.4rem 0.25rem 0.65rem", align="start",
    )


# ============================================================
# MENU ADMIN / USER
# ============================================================

def standard_user_actions() -> rx.Component:
    """
    Ações exibidas para Admin e User.
    """

    return rx.fragment(
        profile_future_item( icon="history", label="Últimas edições",),
        profile_menu_item( icon="refresh_cw", label="Atualizar sistema", on_select=( DashboardState.refresh_data),),
    )


# ============================================================
# MENU SUPERADMIN
# ============================================================

def superadmin_actions() -> rx.Component:
    """Ações exclusivas do SuperAdmin."""
    return rx.fragment(
        profile_future_item(icon="history",label="Últimas atualizações",),
        profile_menu_item( icon="users", label="Administração de usuários", on_select=rx.redirect("/admin/usuarios"),),
        profile_future_item( icon="database", label="Banco de dados",),
        profile_future_item( icon="chart_no_axes_column", label="Relatório de acesso",),
        profile_future_item( icon="calendar_clock", label="Agendamento",),
    )


# ============================================================
# CONTEÚDO DO DROPDOWN
# ============================================================

def profile_dropdown_content() -> rx.Component:
    """Conteúdo exibido ao abrir o perfil."""
    return rx.dropdown_menu.content(
        profile_menu_header(),
        rx.dropdown_menu.separator(),
        # ----------------------------------------------------
        # Perfil
        # ----------------------------------------------------
        profile_menu_item(icon="circle_user_round", label="Perfil", on_select=rx.redirect("/admin/perfil"),),
        # ----------------------------------------------------
        # Permissões específicas
        # ----------------------------------------------------
        rx.cond( AuthState.is_superadmin, superadmin_actions(),
            rx.cond( AuthState.is_visitante, rx.fragment(), standard_user_actions(),),
        ),
        rx.dropdown_menu.separator(),
        # ----------------------------------------------------
        # Sair
        # ----------------------------------------------------
        rx.dropdown_menu.item(
            rx.hstack(
                rx.icon( tag="log_out", size=16, color="#EC2024",),
                rx.text( "Sair", color="#EC2024", font_size="0.82rem", font_weight=(FONT_WEIGHT_MEDIUM),
                ),
                spacing="3", align="center",
            ),
            on_select=AuthState.logout, cursor="pointer",
        ),
        width="280px", padding="0.5rem", background=PROFILE_BACKGROUND, border=(f"1px solid {profile_border()}"), box_shadow=( "0 14px 38px " "rgba(0, 0, 0, 0.18)"),
    )


# ============================================================
# TRIGGER
# ============================================================

def profile_trigger() -> rx.Component:
    """Área clicável exibida no Header."""
    return rx.hstack(
        profile_avatar(),
        rx.vstack(
            rx.text(AuthState.current_user_name, color=profile_primary_text(), font_size=FONT_SIZE_SM, font_weight=(FONT_WEIGHT_MEDIUM), white_space="nowrap", max_width="150px", overflow="hidden", text_overflow="ellipsis",),

            rx.text( AuthState.current_role_label, color=profile_secondary_text(), font_size="0.72rem", white_space="nowrap",),
            spacing="0", align="start",
        ),
        rx.icon( tag="chevron_down", size=15, color=profile_secondary_text(),), align="center", spacing="3", cursor="pointer", padding="0.4rem 0.55rem", border_radius="9px", transition="background 0.2s ease", _hover={ "background": PROFILE_HOVER, },
    )


# ============================================================
# PAINEL
# ============================================================

def profile_menu() -> rx.Component:
    """Painel administrativo do usuário."""
    return rx.dropdown_menu.root(
        rx.dropdown_menu.trigger(profile_trigger()),
        profile_dropdown_content(),
    )