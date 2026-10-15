import reflex as rx

from Back_end.access.states.auth_state import AuthState
from Back_end.interface.layouts.admin_layout import admin_layout
from Back_end.interface.state.users.user_management_state import (UserManagementState,)
from Back_end.interface.theme.semantic import (
    BORDER,
    BORDER_DARK,
    DANGER,
    SUCCESS,
    SURFACE,
    SURFACE_DARK,
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)
from Back_end.interface.theme.typography import (
    FONT_FAMILY_PRIMARY,
    FONT_FAMILY_SECUNDARY,
    FONT_WEIGHT_MEDIUM,
    FONT_WEIGHT_SEMIBOLD,
)


PRIMARY_TEXT = rx.color_mode_cond(
    TEXT_PRIMARY,
    TEXT_PRIMARY_DARK,
)

SECONDARY_TEXT = rx.color_mode_cond(
    TEXT_SECONDARY,
    TEXT_SECONDARY_DARK,
)

CARD_BACKGROUND = rx.color_mode_cond(
    SURFACE,
    SURFACE_DARK,
)

CARD_BORDER = rx.color_mode_cond(
    BORDER,
    BORDER_DARK,
)

CARD_BORDER_STYLE = rx.color_mode_cond(
    f"1px solid {BORDER}",
    f"1px solid {BORDER_DARK}",
)

INPUT_BACKGROUND = rx.color_mode_cond(
    "#FFFFFF",
    "#202844",
)

SOFT_BACKGROUND = rx.color_mode_cond(
    "#F6F8FB",
    "#202844",
)


# ============================================================
# HELPERS VISUAIS
# ============================================================

def role_color(role):
    return rx.cond(
        role == "superadmin",
        "#7C3AED",
        rx.cond(
            role == "admin",
            "#124E8A",
            rx.cond(
                role == "user",
                "#1287B2",
                "#667085",
            ),
        ),
    )


def role_background(role):
    return rx.cond(
        role == "superadmin",
        "rgba(124, 58, 237, 0.10)",
        rx.cond(
            role == "admin",
            "rgba(18, 78, 138, 0.10)",
            rx.cond(
                role == "user",
                "rgba(18, 135, 178, 0.10)",
                "rgba(102, 112, 133, 0.10)",
            ),
        ),
    )


def summary_card(
    icon: str,
    title: str,
    value,
    description: str,
    accent: str,
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(
                    tag=icon,
                    size=19,
                    color=accent,
                ),
                width="40px",
                height="40px",
                min_width="40px",
                border_radius="10px",
                background=(
                    f"color-mix(in srgb, {accent} 10%, transparent)"
                ),
            ),
            rx.vstack(
                rx.text(
                    value,
                    color=PRIMARY_TEXT,
                    font_size="1.25rem",
                    font_weight=FONT_WEIGHT_SEMIBOLD,
                    line_height="1",
                ),
                rx.text(
                    title,
                    color=PRIMARY_TEXT,
                    font_size="0.78rem",
                    font_weight=FONT_WEIGHT_MEDIUM,
                ),
                rx.text(
                    description,
                    color=SECONDARY_TEXT,
                    font_size="0.66rem",
                ),
                spacing="1",
                align="start",
            ),
            align="center",
            spacing="3",
        ),
        background=CARD_BACKGROUND,
        border=CARD_BORDER_STYLE,
        border_radius="12px",
        padding="1rem",
        width="100%",
    )


def role_badge(user) -> rx.Component:
    return rx.box(
        rx.text(
            user["role_label"],
            color=role_color(user["role"]),
            font_size="0.72rem",
            font_weight=FONT_WEIGHT_SEMIBOLD,
        ),
        background=role_background(user["role"]),
        border_radius="999px",
        padding="0.28rem 0.6rem",
        width="fit-content",
        white_space="nowrap",
    )


def status_badge(user) -> rx.Component:
    return rx.cond(
        user["is_active"],
        rx.hstack(
            rx.box(
                width="7px",
                height="7px",
                border_radius="50%",
                background=SUCCESS,
            ),
            rx.text(
                "Ativo",
                color=SUCCESS,
                font_size="0.72rem",
                font_weight=FONT_WEIGHT_MEDIUM,
            ),
            spacing="2",
            align="center",
        ),
        rx.hstack(
            rx.box(
                width="7px",
                height="7px",
                border_radius="50%",
                background=DANGER,
            ),
            rx.text(
                "Inativo",
                color=DANGER,
                font_size="0.72rem",
                font_weight=FONT_WEIGHT_MEDIUM,
            ),
            spacing="2",
            align="center",
        ),
    )


# ============================================================
# CABEÇALHO
# ============================================================

def users_header() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.text(
                "USUÁRIOS",
                color=PRIMARY_TEXT,
                font_family=FONT_FAMILY_SECUNDARY,
                font_size="2.35rem",
                line_height="1",
            ),
            rx.text(
                "Cadastre contas, altere perfis e controle quem pode acessar o painel.",
                color=SECONDARY_TEXT,
                font_family=FONT_FAMILY_PRIMARY,
                font_size="0.85rem",
            ),
            spacing="2",
            align="start",
        ),
        rx.spacer(),
        rx.button(
            rx.icon(
                tag="user_plus",
                size=17,
            ),
            "Novo usuário",
            on_click=UserManagementState.open_create,
            background="#272361",
            color="white",
            border_radius="8px",
            padding_x="1rem",
            cursor="pointer",
            _hover={
                "background": "#124E8A",
            },
        ),
        direction={
            "initial": "column",
            "md": "row",
        },
        width="100%",
        gap="4",
        align={
            "initial": "stretch",
            "md": "center",
        },
    )


# ============================================================
# RESUMO
# ============================================================

def users_summary() -> rx.Component:
    return rx.grid(
        summary_card(
            icon="users",
            title="Total",
            value=UserManagementState.total_users,
            description="Contas cadastradas",
            accent="#272361",
        ),
        summary_card(
            icon="shield_check",
            title="Administradores",
            value=UserManagementState.administrator_users,
            description="Admin + SuperAdmin",
            accent="#7C3AED",
        ),
        summary_card(
            icon="circle_check",
            title="Ativos",
            value=UserManagementState.active_users,
            description="Podem entrar no sistema",
            accent="#288140",
        ),
        summary_card(
            icon="circle_x",
            title="Inativos",
            value=UserManagementState.inactive_users,
            description="Acesso bloqueado",
            accent="#EC2024",
        ),
        columns={
            "initial": "1",
            "sm": "2",
            "xl": "4",
        },
        spacing="3",
        width="100%",
    )


# ============================================================
# MENSAGENS
# ============================================================

def users_messages() -> rx.Component:
    return rx.vstack(
        rx.cond(
            UserManagementState.user_success_message != "",
            rx.hstack(
                rx.icon(
                    tag="circle_check",
                    size=17,
                    color=SUCCESS,
                ),
                rx.text(
                    UserManagementState.user_success_message,
                    color=SUCCESS,
                    font_size="0.8rem",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="x", size=14),
                    on_click=UserManagementState.clear_user_success_message,
                    background="transparent",
                    color=SUCCESS,
                    padding="0.2rem",
                    min_width="auto",
                    height="auto",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
            ),
        ),
        rx.cond(
            UserManagementState.user_error_message != "",
            rx.hstack(
                rx.icon(
                    tag="triangle_alert",
                    size=17,
                    color=DANGER,
                ),
                rx.text(
                    UserManagementState.user_error_message,
                    color=DANGER,
                    font_size="0.8rem",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="x", size=14),
                    on_click=UserManagementState.clear_user_error_message,
                    background="transparent",
                    color=DANGER,
                    padding="0.2rem",
                    min_width="auto",
                    height="auto",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
            ),
        ),
        width="100%",
        spacing="2",
    )


# ============================================================
# CONFIRMAÇÃO DE EXCLUSÃO
# ============================================================

def delete_confirmation() -> rx.Component:
    return rx.cond(
        UserManagementState.delete_confirm_open,
        rx.box(
            rx.flex(
                rx.hstack(
                    rx.center(
                        rx.icon(
                            tag="trash_2",
                            size=18,
                            color=DANGER,
                        ),
                        width="38px",
                        height="38px",
                        min_width="38px",
                        border_radius="9px",
                        background="rgba(236, 32, 36, 0.10)",
                    ),
                    rx.vstack(
                        rx.text(
                            "Excluir usuário permanentemente?",
                            color=PRIMARY_TEXT,
                            font_size="0.82rem",
                            font_weight=FONT_WEIGHT_SEMIBOLD,
                        ),
                        rx.text(
                            "A conta de ",
                            UserManagementState.delete_user_name,
                            " será removida e as sessões serão encerradas.",
                            color=SECONDARY_TEXT,
                            font_size="0.72rem",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    align="center",
                    spacing="3",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=UserManagementState.cancel_delete,
                        variant="soft",
                        cursor="pointer",
                    ),
                    rx.button(
                        rx.icon(tag="trash_2", size=15),
                        rx.cond(
                            UserManagementState.saving,
                            "Excluindo...",
                            "Excluir",
                        ),
                        on_click=UserManagementState.confirm_delete,
                        background=DANGER,
                        color="white",
                        cursor="pointer",
                        disabled=UserManagementState.saving,
                    ),
                    spacing="2",
                ),
                direction={
                    "initial": "column",
                    "lg": "row",
                },
                align={
                    "initial": "stretch",
                    "lg": "center",
                },
                width="100%",
                gap="4",
            ),
            width="100%",
            padding="1rem",
            border="1px solid rgba(236, 32, 36, 0.25)",
            border_left="4px solid #EC2024",
            background=CARD_BACKGROUND,
            border_radius="10px",
        ),
        rx.fragment(),
    )


# ============================================================
# FILTROS
# ============================================================

def users_filters() -> rx.Component:
    return rx.flex(
        rx.input(
            rx.input.slot(
                rx.icon(
                    tag="search",
                    size=16,
                    color=SECONDARY_TEXT,
                ),
            ),
            placeholder="Buscar por nome ou e-mail...",
            value=UserManagementState.search_text,
            on_change=UserManagementState.update_search_text,
            width={
                "initial": "100%",
                "lg": "320px",
            },
            background=INPUT_BACKGROUND,
            border=CARD_BORDER_STYLE,
        ),
        rx.select.root(
            rx.select.trigger(
                width="170px",
                background=INPUT_BACKGROUND,
            ),
            rx.select.content(
                rx.select.item(
                    "Todos os perfis",
                    value="all",
                ),
                rx.select.item(
                    "SuperAdmin",
                    value="superadmin",
                ),
                rx.select.item(
                    "Administrador",
                    value="admin",
                ),
                rx.select.item(
                    "Usuário",
                    value="user",
                ),
                rx.select.item(
                    "Visitante",
                    value="visitante",
                ),
            ),
            value=UserManagementState.role_filter,
            on_change=UserManagementState.update_role_filter,
        ),
        rx.select.root(
            rx.select.trigger(
                width="145px",
                background=INPUT_BACKGROUND,
            ),
            rx.select.content(
                rx.select.item(
                    "Todos",
                    value="all",
                ),
                rx.select.item(
                    "Ativos",
                    value="active",
                ),
                rx.select.item(
                    "Inativos",
                    value="inactive",
                ),
            ),
            value=UserManagementState.status_filter,
            on_change=UserManagementState.update_status_filter,
        ),
        rx.button(
            rx.icon(
                tag="filter_x",
                size=15,
            ),
            "Limpar",
            on_click=UserManagementState.clear_filters,
            variant="ghost",
            color=SECONDARY_TEXT,
            cursor="pointer",
        ),
        rx.spacer(),
        rx.text(
            UserManagementState.result_count,
            " usuário(s)",
            color=SECONDARY_TEXT,
            font_size="0.75rem",
        ),
        direction={
            "initial": "column",
            "lg": "row",
        },
        align={
            "initial": "stretch",
            "lg": "center",
        },
        width="100%",
        gap="3",
    )


# ============================================================
# AÇÕES DA LINHA
# ============================================================

def user_actions(user) -> rx.Component:
    buttons = rx.hstack(
        rx.button(
            rx.icon(
                tag="pencil",
                size=15,
            ),
            on_click=UserManagementState.open_edit(
                user["id"]
            ),
            title="Editar usuário",
            variant="ghost",
            color="#124E8A",
            padding="0.4rem",
            min_width="34px",
            height="34px",
            cursor="pointer",
        ),
        rx.cond(
            AuthState.is_superadmin,
            rx.button(
                rx.icon(
                    tag="trash_2",
                    size=15,
                ),
                on_click=UserManagementState.request_delete(
                    user["id"]
                ),
                title="Excluir usuário",
                variant="ghost",
                color=DANGER,
                padding="0.4rem",
                min_width="34px",
                height="34px",
                cursor="pointer",
            ),
            rx.fragment(),
        ),
        spacing="1",
        justify="end",
        align="center",
    )

    protected = rx.text(
        "Protegido",
        color=SECONDARY_TEXT,
        font_size="0.7rem",
    )

    own_account = rx.text(
        "Sua conta",
        color="#1287B2",
        font_size="0.7rem",
        font_weight=FONT_WEIGHT_MEDIUM,
    )

    return rx.cond(
        user["id"] == AuthState.current_user_id,
        own_account,
        rx.cond(
            user["role"] == "superadmin",
            rx.cond(
                AuthState.is_superadmin,
                buttons,
                protected,
            ),
            buttons,
        ),
    )


# ============================================================
# TABELA
# ============================================================

def user_row(user) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.hstack(
                rx.center(
                    rx.text(
                        user["initials"],
                        color="white",
                        font_size="0.72rem",
                        font_weight=FONT_WEIGHT_SEMIBOLD,
                    ),
                    width="34px",
                    height="34px",
                    min_width="34px",
                    border_radius="50%",
                    background="#272361",
                ),
                rx.vstack(
                    rx.text(
                        user["name"],
                        color=PRIMARY_TEXT,
                        font_size="0.8rem",
                        font_weight=FONT_WEIGHT_MEDIUM,
                    ),
                    rx.text(
                        user["email"],
                        color=SECONDARY_TEXT,
                        font_size="0.7rem",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
        ),
        rx.table.cell(
            role_badge(user)
        ),
        rx.table.cell(
            status_badge(user)
        ),
        rx.table.cell(
            user_actions(user),
            justify="end",
        ),
        align="center",
    )


def users_table() -> rx.Component:
    return rx.box(
        users_filters(),
        rx.box(
            rx.cond(
                UserManagementState.loading,
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3"),
                        rx.text(
                            "Carregando usuários...",
                            color=SECONDARY_TEXT,
                            font_size="0.78rem",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    width="100%",
                    min_height="220px",
                ),
                rx.cond(
                    UserManagementState.result_count == 0,
                    rx.center(
                        rx.vstack(
                            rx.icon(
                                tag="users",
                                size=28,
                                color=SECONDARY_TEXT,
                            ),
                            rx.text(
                                "Nenhum usuário encontrado.",
                                color=PRIMARY_TEXT,
                                font_size="0.85rem",
                                font_weight=FONT_WEIGHT_MEDIUM,
                            ),
                            rx.text(
                                "Tente mudar os filtros ou cadastre uma nova conta.",
                                color=SECONDARY_TEXT,
                                font_size="0.72rem",
                                text_align="center",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        min_height="220px",
                        width="100%",
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell(
                                    "Usuário",
                                    min_width="260px",
                                ),
                                rx.table.column_header_cell(
                                    "Perfil",
                                    min_width="130px",
                                ),
                                rx.table.column_header_cell(
                                    "Status",
                                    min_width="110px",
                                ),
                                rx.table.column_header_cell(
                                    "Ações",
                                    justify="end",
                                    min_width="90px",
                                ),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                UserManagementState.filtered_users,
                                user_row,
                            ),
                        ),
                        width="100%",
                        variant="ghost",
                        size="2",
                    ),
                ),
            ),
            width="100%",
            overflow_x="auto",
        ),
        width="100%",
        background=CARD_BACKGROUND,
        border=CARD_BORDER_STYLE,
        border_radius="12px",
        padding="1rem",
        display="flex",
        flex_direction="column",
        gap="1rem",
        min_width="0",
    )


# ============================================================
# FORMULÁRIO LATERAL
# ============================================================

def form_label(
    label: str,
    required: bool = False,
) -> rx.Component:
    return rx.text(
        label,
        " *" if required else "",
        color=PRIMARY_TEXT,
        font_size="0.72rem",
        font_weight=FONT_WEIGHT_MEDIUM,
    )


def user_editor() -> rx.Component:
    return rx.cond(
        UserManagementState.editor_open,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            UserManagementState.editor_title,
                            color=PRIMARY_TEXT,
                            font_size="1rem",
                            font_weight=FONT_WEIGHT_SEMIBOLD,
                        ),
                        rx.text(
                            "Os campos com * são obrigatórios.",
                            color=SECONDARY_TEXT,
                            font_size="0.68rem",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon(tag="x", size=16),
                        on_click=UserManagementState.close_editor,
                        background="transparent",
                        color=SECONDARY_TEXT,
                        padding="0.3rem",
                        min_width="auto",
                        height="auto",
                        cursor="pointer",
                    ),
                    width="100%",
                    align="start",
                ),
                rx.box(
                    width="100%",
                    height="1px",
                    background=CARD_BORDER,
                ),
                rx.vstack(
                    form_label("Nome", True),
                    rx.input(
                        placeholder="Nome completo",
                        value=UserManagementState.form_name,
                        on_change=UserManagementState.update_form_name,
                        width="100%",
                        background=INPUT_BACKGROUND,
                    ),
                    width="100%",
                    spacing="2",
                    align="stretch",
                ),
                rx.vstack(
                    form_label("E-mail", True),
                    rx.input(
                        placeholder="usuario@dominio.com",
                        type="email",
                        value=UserManagementState.form_email,
                        on_change=UserManagementState.update_form_email,
                        width="100%",
                        background=INPUT_BACKGROUND,
                    ),
                    width="100%",
                    spacing="2",
                    align="stretch",
                ),
                rx.vstack(
                    rx.text(
                        UserManagementState.password_label,
                        rx.cond(
                            UserManagementState.editor_mode == "create",
                            " *",
                            "",
                        ),
                        color=PRIMARY_TEXT,
                        font_size="0.72rem",
                        font_weight=FONT_WEIGHT_MEDIUM,
                    ),
                    rx.input(
                        placeholder="••••••••",
                        type="password",
                        value=UserManagementState.form_password,
                        on_change=UserManagementState.update_form_password,
                        width="100%",
                        background=INPUT_BACKGROUND,
                    ),
                    rx.text(
                        rx.cond(
                            UserManagementState.editor_mode == "edit",
                            "Deixe em branco para manter a senha atual.",
                            "Use no mínimo 8 caracteres.",
                        ),
                        color=SECONDARY_TEXT,
                        font_size="0.66rem",
                    ),
                    width="100%",
                    spacing="2",
                    align="stretch",
                ),
                rx.vstack(
                    form_label("Perfil de acesso", True),
                    rx.select.root(
                        rx.select.trigger(
                            width="100%",
                            background=INPUT_BACKGROUND,
                        ),
                        rx.select.content(
                            rx.select.item(
                                "SuperAdmin",
                                value="superadmin",
                                disabled=(
                                    AuthState.is_superadmin
                                    == False
                                ),
                            ),
                            rx.select.item(
                                "Administrador",
                                value="admin",
                            ),
                            rx.select.item(
                                "Usuário",
                                value="user",
                            ),
                            rx.select.item(
                                "Visitante",
                                value="visitante",
                            ),
                        ),
                        value=UserManagementState.form_role,
                        on_change=UserManagementState.update_form_role,
                    ),
                    rx.text(
                        "SuperAdmin possui acesso total. Admin gerencia o painel e usuários. Usuário opera conteúdo. Visitante apenas consulta.",
                        color=SECONDARY_TEXT,
                        font_size="0.66rem",
                        line_height="1.4",
                    ),
                    width="100%",
                    spacing="2",
                    align="stretch",
                ),
                rx.vstack(
                    form_label("Status", True),
                    rx.select.root(
                        rx.select.trigger(
                            width="100%",
                            background=INPUT_BACKGROUND,
                        ),
                        rx.select.content(
                            rx.select.item(
                                "Ativo",
                                value="active",
                            ),
                            rx.select.item(
                                "Inativo",
                                value="inactive",
                            ),
                        ),
                        value=UserManagementState.form_status,
                        on_change=UserManagementState.update_form_status,
                    ),
                    rx.text(
                        "Usuários inativos não conseguem entrar no sistema.",
                        color=SECONDARY_TEXT,
                        font_size="0.66rem",
                    ),
                    width="100%",
                    spacing="2",
                    align="stretch",
                ),
                rx.box(
                    width="100%",
                    height="1px",
                    background=CARD_BORDER,
                ),
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        on_click=UserManagementState.close_editor,
                        variant="soft",
                        cursor="pointer",
                        flex="1",
                    ),
                    rx.button(
                        rx.icon(
                            tag="save",
                            size=15,
                        ),
                        rx.cond(
                            UserManagementState.saving,
                            "Salvando...",
                            UserManagementState.editor_submit_label,
                        ),
                        on_click=UserManagementState.save_user,
                        background="#272361",
                        color="white",
                        cursor="pointer",
                        disabled=UserManagementState.saving,
                        flex="1.3",
                        _hover={
                            "background": "#124E8A",
                        },
                    ),
                    width="100%",
                    spacing="2",
                ),
                width="100%",
                spacing="4",
                align="stretch",
            ),
            width={
                "initial": "100%",
                "xl": "380px",
            },
            min_width={
                "initial": "0",
                "xl": "380px",
            },
            background=CARD_BACKGROUND,
            border=CARD_BORDER_STYLE,
            border_radius="12px",
            padding="1.15rem",
            align_self="flex-start",
            position={
                "initial": "static",
                "xl": "sticky",
            },
            top="0",
        ),
        rx.fragment(),
    )


# ============================================================
# PÁGINA
# ============================================================

def users_content() -> rx.Component:
    return rx.vstack(
        users_header(),
        users_summary(),
        users_messages(),
        delete_confirmation(),
        rx.flex(
            users_table(),
            user_editor(),
            direction={
                "initial": "column",
                "xl": "row",
            },
            width="100%",
            gap="4",
            align="start",
        ),
        width="100%",
        spacing="5",
        align="stretch",
        font_family=FONT_FAMILY_PRIMARY,
    )


def users_page() -> rx.Component:
    return admin_layout(
        users_content()
    )
