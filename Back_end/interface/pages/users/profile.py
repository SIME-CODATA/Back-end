import reflex as rx

from Back_end.access.states.auth_state import (AuthState,)
from Back_end.interface.layouts.admin_layout import (admin_layout,)
from Back_end.interface.theme.semantic import ( BORDER, BORDER_DARK, TEXT_PRIMARY, TEXT_PRIMARY_DARK, TEXT_SECONDARY, TEXT_SECONDARY_DARK,)
from Back_end.interface.theme.typography import ( FONT_FAMILY_PRIMARY, FONT_FAMILY_SECUNDARY, FONT_WEIGHT_SEMIBOLD, )

# ============================================================
# CORES
# ============================================================

PRIMARY_TEXT = rx.color_mode_cond(TEXT_PRIMARY,TEXT_PRIMARY_DARK,)
SECONDARY_TEXT = rx.color_mode_cond( TEXT_SECONDARY, TEXT_SECONDARY_DARK, )
PROFILE_BORDER = rx.color_mode_cond( BORDER, BORDER_DARK, )
PROFILE_SURFACE = rx.color_mode_cond( "#FFFFFF", "#1E2948", )

# ============================================================
# LINHA
# ============================================================

def profile_field(label: str,value,) -> rx.Component:
    """Campo somente leitura do perfil."""
    return rx.vstack(
        rx.text( label, color=SECONDARY_TEXT, font_size="0.72rem", font_weight="600", text_transform="uppercase", ),
        rx.text( value, color=PRIMARY_TEXT, font_size="0.92rem", ),
        spacing="1", align="start", width="100%",
    )


# ============================================================
# CONTEÚDO
# ============================================================

def profile_content() -> rx.Component:
    """Perfil do usuário autenticado."""

    return rx.vstack(
        rx.vstack(
            rx.text( "PERFIL", color=PRIMARY_TEXT, font_family=FONT_FAMILY_SECUNDARY, font_size="2.4rem", line_height="1", ),
            rx.text( "Informações da sua conta " "no painel administrativo.", color=SECONDARY_TEXT, font_family=FONT_FAMILY_PRIMARY, font_size="0.85rem", ), spacing="2", align="start",
        ),

        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.center(
                        rx.icon(tag="user",size=24,color="white",),
                        width="58px",height="58px",min_width="58px",border_radius="50%",background="#272361",
                    ),

                    rx.vstack(
                        rx.text(AuthState.current_user_name, color=PRIMARY_TEXT, font_size="1.1rem", font_weight=(FONT_WEIGHT_SEMIBOLD), ),
                        rx.text(AuthState.current_role_label, color="#1287B2", font_size="0.78rem",),
                        spacing="1", align="start",
                    ),
                    spacing="4", align="center",
                ),
                rx.box( width="100%", height="1px", background=PROFILE_BORDER, ),
                rx.grid(
                    profile_field( "Nome", AuthState.current_user_name, ),
                    profile_field( "E-mail", AuthState.current_user_email, ),
                    profile_field( "Perfil de acesso", AuthState.current_role_label, ),
                    profile_field( "ID do usuário", AuthState.current_user_id, ),
                    columns={ "initial": "1", "md": "2", }, spacing="5", width="100%",
                ),
                rx.text(
                    "A edição de nome, senha e outros "
                    "dados será adicionada junto ao "
                    "módulo de administração de usuários.",
                    color=SECONDARY_TEXT,
                    font_size="0.75rem",
                ),
                spacing="5", width="100%", align="stretch",
            ),
            width="100%", max_width="760px", padding="1.5rem", background=PROFILE_SURFACE, border=( f"1px solid {PROFILE_BORDER}" ), border_radius="12px",
        ),
        spacing="5", width="100%", align="start",
    )


# ============================================================
# PÁGINA
# ============================================================

def profile_page() -> rx.Component:
    """Página de perfil."""

    return admin_layout( profile_content() )