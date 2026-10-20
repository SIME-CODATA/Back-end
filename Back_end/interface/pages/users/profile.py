import reflex as rx

from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.state.users.profile_state import (ProfileState,)
from Back_end.interface.theme.semantic import (
    BORDER,
    BORDER_DARK,
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)
from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
    FONT_WEIGHT_SEMIBOLD,
)


PRIMARY_TEXT = rx.color_mode_cond(TEXT_PRIMARY, TEXT_PRIMARY_DARK)
SECONDARY_TEXT = rx.color_mode_cond(TEXT_SECONDARY, TEXT_SECONDARY_DARK)
PROFILE_BORDER = rx.color_mode_cond(BORDER, BORDER_DARK)
PROFILE_SURFACE = rx.color_mode_cond("#FFFFFF", "#1E2948")
INPUT_BACKGROUND = rx.color_mode_cond("#FFFFFF", "#18233F")
ACTIVITY_BACKGROUND = rx.color_mode_cond("#F8FAFC", "#18233F")


def profile_field(label: str, value) -> rx.Component:
    return rx.vstack(
        rx.text(
            label,
            color=SECONDARY_TEXT,
            font_size="0.72rem",
            font_weight="600",
            text_transform="uppercase",
        ),
        rx.text(value, color=PRIMARY_TEXT, font_size="0.92rem"),
        spacing="1",
        align="start",
        width="100%",
    )


def section_header(title: str, description: str) -> rx.Component:
    return rx.vstack(
        rx.text(
            title,
            color=PRIMARY_TEXT,
            font_size="1rem",
            font_weight=FONT_WEIGHT_SEMIBOLD,
        ),
        rx.text(
            description,
            color=SECONDARY_TEXT,
            font_size="0.76rem",
        ),
        spacing="1",
        align="start",
        width="100%",
    )


def activity_item(item) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.icon(tag="history", size=16, color="#1287B2"),
            width="34px",
            height="34px",
            min_width="34px",
            border_radius="9px",
            background=rx.color_mode_cond(
                "rgba(18, 135, 178, 0.09)",
                "rgba(76, 199, 226, 0.12)",
            ),
        ),
        rx.vstack(
            rx.hstack(
                rx.text(
                    item["action_label"],
                    color=PRIMARY_TEXT,
                    font_size="0.82rem",
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                ),
                rx.spacer(),
                rx.text(
                    item["created_at"],
                    color=SECONDARY_TEXT,
                    font_size="0.68rem",
                    white_space="nowrap",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                item["description"],
                color=SECONDARY_TEXT,
                font_size="0.75rem",
                line_height="1.4",
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        width="100%",
        align="start",
        spacing="3",
        padding="0.8rem",
        background=ACTIVITY_BACKGROUND,
        border_radius="10px",
    )


def system_update_item(item) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.icon(tag="history", size=16, color="#067FD0"),
            width="34px",
            height="34px",
            min_width="34px",
            border_radius="9px",
            background=rx.color_mode_cond(
                "rgba(39, 35, 97, 0.08)",
                "rgba(255, 255, 255, 0.08)",
            ),
        ),
        rx.vstack(
            rx.hstack(
                rx.text(
                    item["action_label"],
                    color=PRIMARY_TEXT,
                    font_size="0.82rem",
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                ),
                rx.spacer(),
                rx.text(
                    item["created_at"],
                    color=SECONDARY_TEXT,
                    font_size="0.68rem",
                    white_space="nowrap",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                item["description"],
                color=SECONDARY_TEXT,
                font_size="0.75rem",
                line_height="1.4",
            ),
            rx.text(
                item["actor_name"],
                " • ",
                item["actor_email"],
                color=SECONDARY_TEXT,
                font_size="0.67rem",
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        width="100%",
        align="start",
        spacing="3",
        padding="0.8rem",
        background=ACTIVITY_BACKGROUND,
        border_radius="10px",
    )


def account_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon(tag="user", size=24, color="white"),
                    width="58px",
                    height="58px",
                    min_width="58px",
                    border_radius="50%",
                    background="#272361",
                ),
                rx.vstack(
                    rx.text(
                        ProfileState.profile_name,
                        color=PRIMARY_TEXT,
                        font_size="1.1rem",
                        font_weight=FONT_WEIGHT_SEMIBOLD,
                    ),
                    rx.text(
                        ProfileState.profile_role_label,
                        color="#1287B2",
                        font_size="0.78rem",
                    ),
                    spacing="1",
                    align="start",
                ),
                spacing="4",
                align="center",
            ),
            rx.box(width="100%", height="1px", background=PROFILE_BORDER),
            rx.grid(
                profile_field("Nome", ProfileState.profile_name),
                profile_field("E-mail", ProfileState.profile_email),
                profile_field("Perfil de acesso", ProfileState.profile_role_label),
                profile_field("ID do usuário", ProfileState.profile_user_id),
                columns={"initial": "1", "md": "2"},
                spacing="5",
                width="100%",
            ),
            rx.text(
                "Nome, e-mail, perfil e status são administrados pela gestão "
                "de usuários. Neste perfil você pode consultar suas atividades "
                "e alterar sua própria senha.",
                color=SECONDARY_TEXT,
                font_size="0.75rem",
            ),
            spacing="5",
            width="100%",
            align="stretch",
        ),
        width="100%",
        padding="1.5rem",
        background=PROFILE_SURFACE,
        border=f"1px solid {PROFILE_BORDER}",
        border_radius="12px",
    )


def password_input(label: str, placeholder: str, value, on_change) -> rx.Component:
    return rx.vstack(
        rx.text(
            label,
            color=PRIMARY_TEXT,
            font_size="0.78rem",
            font_weight="600",
        ),
        rx.input(
            value=value,
            on_change=on_change,
            type="password",
            placeholder=placeholder,
            width="100%",
            height="42px",
            background=INPUT_BACKGROUND,
            border=f"1px solid {PROFILE_BORDER}",
            border_radius="9px",
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def security_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            section_header("Segurança", "Altere a senha da sua própria conta."),
            rx.grid(
                password_input(
                    "Senha atual",
                    "Digite sua senha atual",
                    ProfileState.current_password,
                    ProfileState.update_current_password,
                ),
                password_input(
                    "Nova senha",
                    "Mínimo de 8 caracteres",
                    ProfileState.new_password,
                    ProfileState.update_new_password,
                ),
                password_input(
                    "Confirmar nova senha",
                    "Digite novamente a nova senha",
                    ProfileState.confirm_password,
                    ProfileState.update_confirm_password,
                ),
                columns={"initial": "1", "md": "3"},
                spacing="4",
                width="100%",
            ),
            rx.cond(
                ProfileState.password_error_message != "",
                rx.callout(
                    ProfileState.password_error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    width="100%",
                ),
                rx.fragment(),
            ),
            rx.cond(
                ProfileState.password_success_message != "",
                rx.callout(
                    ProfileState.password_success_message,
                    icon="circle_check",
                    color_scheme="green",
                    width="100%",
                ),
                rx.fragment(),
            ),
            rx.hstack(
                rx.text(
                    "Ao alterar a senha, as outras sessões abertas da sua "
                    "conta serão encerradas.",
                    color=SECONDARY_TEXT,
                    font_size="0.72rem",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="key", size=15),
                    "Alterar senha",
                    on_click=ProfileState.change_password,
                    disabled=ProfileState.changing_password,
                    background="#272361",
                    color="white",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
            ),
            spacing="5",
            width="100%",
            align="stretch",
        ),
        width="100%",
        padding="1.5rem",
        background=PROFILE_SURFACE,
        border=f"1px solid {PROFILE_BORDER}",
        border_radius="12px",
    )


def activities_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            section_header(
                "Minhas atividades",
                "As 10 ações mais recentes realizadas pela sua conta.",
            ),
            rx.cond(
                ProfileState.has_activities,
                rx.vstack(
                    rx.foreach(ProfileState.activities, activity_item),
                    spacing="2",
                    width="100%",
                ),
                rx.center(
                    rx.text(
                        "Nenhuma atividade registrada ainda.",
                        color=SECONDARY_TEXT,
                        font_size="0.8rem",
                    ),
                    width="100%",
                    padding="1.5rem",
                ),
            ),
            spacing="4",
            width="100%",
            align="stretch",
        ),
        id="atividades",
        width="100%",
        padding="1.5rem",
        background=PROFILE_SURFACE,
        border=f"1px solid {PROFILE_BORDER}",
        border_radius="12px",
    )


def system_updates_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            section_header(
                "Últimas atualizações do sistema",
                "Atividades administrativas recentes registradas pela auditoria.",
            ),
            rx.cond(
                ProfileState.has_system_updates,
                rx.vstack(
                    rx.foreach(ProfileState.system_updates, system_update_item),
                    spacing="2",
                    width="100%",
                ),
                rx.center(
                    rx.text(
                        "Nenhuma atualização registrada ainda.",
                        color=SECONDARY_TEXT,
                        font_size="0.8rem",
                    ),
                    width="100%",
                    padding="1.5rem",
                ),
            ),
            spacing="4",
            width="100%",
            align="stretch",
        ),
        id="atualizacoes",
        width="100%",
        padding="1.5rem",
        background=PROFILE_SURFACE,
        border=f"1px solid {PROFILE_BORDER}",
        border_radius="12px",
    )


def profile_content() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text(
                "PERFIL",
                color=PRIMARY_TEXT,
                font_family=FONT_FAMILY_SECUNDARY,
                font_size="2.4rem",
                line_height="1",
            ),
            rx.text(
                "Dados da conta, segurança e histórico de atividades.",
                color=SECONDARY_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.85rem",
            ),
            spacing="2",
            align="start",
        ),
        rx.cond(
            ProfileState.profile_error_message != "",
            rx.callout(
                ProfileState.profile_error_message,
                icon="triangle_alert",
                color_scheme="red",
                width="100%",
            ),
            rx.fragment(),
        ),
        rx.grid(
            account_card(),
            security_card(),
            columns={"initial": "1", "xl": "2"},
            spacing="5",
            width="100%",
        ),
        activities_card(),
        rx.cond(
            ProfileState.show_system_updates,
            system_updates_card(),
            rx.fragment(),
        ),
        spacing="5",
        width="100%",
        align="start",
    )


def profile_page() -> rx.Component:
    return admin_layout(profile_content())
